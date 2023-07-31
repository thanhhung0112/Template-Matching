using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Globalization;
using System.Drawing.Imaging;
using System.Net.Http;
using System.Net.Sockets;
using System.Net;
using System.Threading;

using NeptuneC_Interface;
using System.Security.AccessControl;
using System.Drawing.Drawing2D;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace WinFormCVU
{
    public partial class ComputerVisionUI : Form
    {
        private NeptuneC_Interface.NeptuneCUnplugCallback DeviceUnplugCallbackInst;
        private NeptuneC_Interface.NeptuneCFrameCallback FrameCallbackInst;

        string targetImagePath;
        string templatePath;

        Stopwatch stopwatch = new Stopwatch();

        string defaultDirectory = $"{Application.StartupPath}\\";
        string stream_folder = "Stream_camera";
        string output_folder = "Output";
        string template_folder = "Template";

        // these are all variables used in RoI selection 
        private bool isSelecting = false;
        private Rectangle rect;
        private Point startPoint;
        private int cornerSize = 5;
        private Rectangle selectedRect;
        private bool isReshape = false;

        // this is a variable used in zoom in or zoom out
        private bool isResizing = false;

        private TcpListener serverSocket;
        private Thread serverThread;
        private bool isRunning;
        private TcpListener serverSocket2;
        private Thread serverThread2;
        private bool isRunning2;
        private TcpListener serverSocket3;
        private Thread serverThread3;
        private bool isRunning3;
        private List<float[]> sharedData = new List<float[]>();
        private TaskCompletionSource<bool> matchTemplateCompletionSource;

        // this is a variable used in camera connection
        public IntPtr m_pCameraHandle = IntPtr.Zero;
        private NEPTUNE_FEATURE[] m_arrFeatureInfo;
        private CheckBox[] m_arrCheckBox;
        private ENeptuneFeature[] m_arrMapping = new ENeptuneFeature[]
        {
            ENeptuneFeature.NEPTUNE_FEATURE_GAMMA,
            ENeptuneFeature.NEPTUNE_FEATURE_GAIN,
            ENeptuneFeature.NEPTUNE_FEATURE_RGAIN,
            ENeptuneFeature.NEPTUNE_FEATURE_GGAIN,
            ENeptuneFeature.NEPTUNE_FEATURE_BGAIN,
            ENeptuneFeature.NEPTUNE_FEATURE_AUTOGAIN_MIN,
            ENeptuneFeature.NEPTUNE_FEATURE_AUTOGAIN_MAX,
            ENeptuneFeature.NEPTUNE_FEATURE_SHUTTER,
            ENeptuneFeature.NEPTUNE_FEATURE_AUTOSHUTTER_MIN,
            ENeptuneFeature.NEPTUNE_FEATURE_AUTOSHUTTER_MAX,
            ENeptuneFeature.NEPTUNE_FEATURE_AUTOEXPOSURE,
            ENeptuneFeature.NEPTUNE_FEATURE_BLACKLEVEL,
            ENeptuneFeature.NEPTUNE_FEATURE_CONTRAST,
            ENeptuneFeature.NEPTUNE_FEATURE_HUE,
            ENeptuneFeature.NEPTUNE_FEATURE_SATURATION,
            ENeptuneFeature.NEPTUNE_FEATURE_SHARPNESS,
            ENeptuneFeature.NEPTUNE_FEATURE_TRIGNOISEFILTER,
            ENeptuneFeature.NEPTUNE_FEATURE_BRIGHTLEVELIRIS,
            ENeptuneFeature.NEPTUNE_FEATURE_SNOWNOISEREMOVE,
            ENeptuneFeature.NEPTUNE_FEATURE_OPTFILTER,
            ENeptuneFeature.NEPTUNE_FEATURE_PAN,
            ENeptuneFeature.NEPTUNE_FEATURE_TILT,
            ENeptuneFeature.NEPTUNE_FEATURE_LCD_BLUE_GAIN,
            ENeptuneFeature.NEPTUNE_FEATURE_LCD_RED_GAIN,
            ENeptuneFeature.NEPTUNE_FEATURE_WHITEBALANCE
        };

        public ComputerVisionUI()
        {
            InitializeComponent();
        }

        private void ComputerVisionUI_Load(object sender, EventArgs e)
        {
            Template_box.AllowDrop = true;
            Image_box.AllowDrop = true;
            Similarity_score.Text = "0.95";
            Overlap.Text = "0.4";
            Min_modify.Text = "-20";
            Max_modify.Text = "20";
            Scale_ratio.Text = "20";
            Method_similarity.Text = "cv2.TM_CCORR_NORMED";
            conf_score.Text = "0.75";
            img_size.Text = "750";
            serverIP.Text = "192.168.176.1";

            Cam_capture.Enabled = false;
            Match_template.Enabled = false;
            add_template.Enabled = false;
            down_scale.Enabled = false;
            up_scale.Enabled = false;
            Elasped_time.ReadOnly = true;
            CVU_status.ReadOnly = true;
            serverStatus.ReadOnly = true;

            InitCameraList();
        }

        private void ComputerVisionUI_FormClosing(object sender, FormClosingEventArgs e)
        {
            CloseCameraHandle();
            NeptuneC.ntcUninit();

            DisconnectServer();
        }

        public class ItemData
        {
            public String m_strLabel = "";
            public Int32 m_nValue = 0;
            public NEPTUNE_CAM_INFO m_stCameraInfo;

            public ItemData(String strLabel, Int32 nValue)
            {
                m_strLabel = strLabel;
                m_nValue = nValue;
            }

            public ItemData(NEPTUNE_CAM_INFO stCameraInfo)
            {
                m_stCameraInfo = stCameraInfo;
                m_strLabel = m_stCameraInfo.strVendor + ": [" + m_stCameraInfo.strSerial + "] " + m_stCameraInfo.strModel;
            }

            public override String ToString()
            {
                return m_strLabel;
            }
        };

        private void CloseCameraHandle()
        {
            if (m_pCameraHandle != IntPtr.Zero)
            {
                NeptuneC.ntcClose(m_pCameraHandle);
                m_pCameraHandle = IntPtr.Zero;
            }
        }

        private void My_Refresh_Click(object sender, EventArgs e)
        {
            InitCameraList();
        }

        private void InitCameraList()
        {
            NeptuneC.ntcInit();
            ItemData CurSelItem = (ItemData)m_cbCameraList.SelectedItem;

            m_cbCameraList.Items.Clear();

            UInt32 uiCount = 0;
            if (NeptuneC.ntcGetCameraCount(ref uiCount) == ENeptuneError.NEPTUNE_ERR_Success)
            {
                if (uiCount > 0)
                {
                    NEPTUNE_CAM_INFO[] pCameraInfo = new NEPTUNE_CAM_INFO[uiCount];
                    ENeptuneError emErr = NeptuneC.ntcGetCameraInfo(pCameraInfo, uiCount);
                    if (emErr == ENeptuneError.NEPTUNE_ERR_Success)
                    {
                        for (UInt32 i = 0; i < uiCount; i++)
                        {
                            Int32 nItem = m_cbCameraList.Items.Add(new ItemData(pCameraInfo[i]));
                            if (CurSelItem != null)
                            {
                                if (((ItemData)m_cbCameraList.Items[nItem]).m_stCameraInfo.strSerial.Equals(CurSelItem.m_stCameraInfo.strSerial) == true)
                                {
                                    m_cbCameraList.SelectedIndex = nItem;
                                }
                            }
                        }
                    }
                }
            }

            if (CurSelItem != null && m_cbCameraList.SelectedIndex == -1)
            {
                CloseCameraHandle();
            }
        }

        private void m_cbCameraList_SelectedIndexChanged(object sender, EventArgs e)
        {
            CloseCameraHandle();

            if (m_cbCameraList.SelectedIndex != -1)
            {
                ENeptuneError emErr = NeptuneC.ntcOpen(((ItemData)m_cbCameraList.SelectedItem).m_stCameraInfo.strCamID, ref m_pCameraHandle, ENeptuneDevAccess.NEPTUNE_DEV_ACCESS_EXCLUSIVE);
                if (emErr == ENeptuneError.NEPTUNE_ERR_Success)
                {
                    //NeptuneC.ntcSetDisplay(m_pCameraHandle, Image_box.Handle);
                    NeptuneC.ntcSetUnplugCallback(m_pCameraHandle, DeviceUnplugCallbackInst, this.Handle);
                    NeptuneC.ntcSetFrameCallback(m_pCameraHandle, FrameCallbackInst, this.Handle);
                }

                _ = NeptuneC.ntcSetAcquisition(m_pCameraHandle, ENeptuneBoolean.NEPTUNE_BOOL_TRUE);

                Int32 nEffectFlags = 0;
                if (NeptuneC.ntcGetEffect(m_pCameraHandle, ref nEffectFlags) == ENeptuneError.NEPTUNE_ERR_Success)
                {
                    nEffectFlags |= (Int32)ENeptuneEffect.NEPTUNE_EFFECT_FLIP;

                    _ = NeptuneC.ntcSetEffect(m_pCameraHandle, nEffectFlags);
                }

                Cam_capture.Enabled = true;
                NEPTUNE_IMAGE_SIZE stImageSize = new NEPTUNE_IMAGE_SIZE();
                stImageSize.nStartX = 0;
                stImageSize.nStartY = 0;
                stImageSize.nSizeX = 3220;
                stImageSize.nSizeY = 3448;
                _ = NeptuneC.ntcSetImageSize(m_pCameraHandle, stImageSize);

                ENeptuneError emErr1 = NeptuneC.ntcSetPixelFormat(m_pCameraHandle, (ENeptunePixelFormat)108);

                NEPTUNE_FEATURE stInfo = new NEPTUNE_FEATURE();
                m_arrFeatureInfo = new NEPTUNE_FEATURE[m_arrMapping.Length];
                stInfo = m_arrFeatureInfo[m_arrMapping.Length - 1];
                stInfo.AutoMode = ENeptuneAutoMode.NEPTUNE_AUTO_OFF;
                NeptuneC.ntcSetFeature(m_pCameraHandle, m_arrMapping[m_arrMapping.Length - 1], stInfo);

                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Gamma", (int)0);

                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Gain", (int)0);

                // Red
                stInfo = m_arrFeatureInfo[2];
                stInfo.Value = 469;
                NeptuneC.ntcSetFeature(m_pCameraHandle, m_arrMapping[2], stInfo);

                // Green
                stInfo = m_arrFeatureInfo[3];
                stInfo.Value = 363;
                NeptuneC.ntcSetFeature(m_pCameraHandle, m_arrMapping[3], stInfo);

                // Blue
                stInfo = m_arrFeatureInfo[4];
                stInfo.Value = 874;
                NeptuneC.ntcSetFeature(m_pCameraHandle, m_arrMapping[4], stInfo);

                //108
                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "BlackLevel", (int)28);

                //435
                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Contrast", (int)300);

                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Hue", (int)255);

                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Saturation", (int)255);

                NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Sharpness", (int)0);

                //m_arrCheckBox = new CheckBox[m_arrMapping.Length - 1];
                //stInfo = m_arrFeatureInfo[7];
                //stInfo.bOnOff = ENeptuneBoolean.NEPTUNE_BOOL_TRUE;
                //stInfo.Value = 47900;
                //NeptuneC.ntcSetFeature(m_pCameraHandle, m_arrMapping[7], stInfo);

                //stInfo = m_arrFeatureInfo[7];
                //stInfo.Value = 47900;
                //ENeptuneError emErr1 = NeptuneC.ntcSetFeature(m_pCameraHandle, m_arrMapping[7], stInfo);
                //MessageBox.Show($"{emErr1}");
                //NeptuneC.ntcSetNodeInt(m_pCameraHandle, "Shutter", (int)47900);
            }
        }

        private async Task captureFrame()
        {
            if (m_pCameraHandle != IntPtr.Zero)
            {
                if (!Directory.Exists(Path.Combine(defaultDirectory, stream_folder)))
                {
                    Directory.CreateDirectory(Path.Combine(defaultDirectory, stream_folder));
                }

                else
                {
                    DirectoryInfo directory = new DirectoryInfo(Path.Combine(defaultDirectory, stream_folder));

                    // Delete all files within the folder
                    foreach (FileInfo file in directory.GetFiles())
                    {
                        file.Delete();
                    }
                }
                string cameraPath = Path.Combine(defaultDirectory, Path.Combine(stream_folder, "input_image.jpg"));
                _ = await Task.Run(() => NeptuneC.ntcSaveImage(m_pCameraHandle, cameraPath, 50));
            }
        }

        private void Template_box_DragDrop(object sender, DragEventArgs e)
        {
            string[] files = (string[])e.Data.GetData(DataFormats.FileDrop);
            if (files.Length > 0)
            {
                string imagePath = files[0];
                Template_box.ImageLocation = imagePath;
                string fullTemplatePath = imagePath;
                templatePath = get_relativePath(fullTemplatePath, defaultDirectory);

                string templatePathCopy = Path.Combine(Path.GetDirectoryName(templatePath), "copy_" + Path.GetFileName(templatePath));
                File.Copy(templatePath, templatePathCopy, true);

                ShowImage(templatePathCopy, Template_box);

                File.Delete(templatePathCopy);
            }
        }

        private void Template_box_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                e.Effect = DragDropEffects.Copy;
            }
        }

        private void Image_box_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                string[] file = (string[])e.Data.GetData(DataFormats.FileDrop);
                if (file.Length == 1 && (Path.GetExtension(file[0]).ToLower() == ".png" || Path.GetExtension(file[0]).ToLower() == ".jpg" || Path.GetExtension(file[0]).ToLower() == ".jpeg" || Path.GetExtension(file[0]).ToLower() == ".bmp" || Path.GetExtension(file[0]).ToLower() == ".gif"))
                {
                    e.Effect = DragDropEffects.Copy;
                }
            }
        }

        private void Image_box_DragDrop(object sender, DragEventArgs e)
        {
            string[] file = (string[])e.Data.GetData(DataFormats.FileDrop);
            if (file.Length > 0)
            {
                string imagePath = file[0];
                string fullTargetImagePath = imagePath;
                targetImagePath = get_relativePath(fullTargetImagePath, defaultDirectory);

                string targetImagePathCopy = Path.Combine(Path.GetDirectoryName(targetImagePath), "copy_" + Path.GetFileName(targetImagePath));
                File.Copy(targetImagePath, targetImagePathCopy, true);

                ShowImage(targetImagePathCopy, Image_box);

                File.Delete(targetImagePathCopy);
            }
        }

        private void LoadCsvToDataGridView(string csvFilePath, DataGridView dataGridView)
        {
            if (!File.Exists(Path.Combine(defaultDirectory, csvFilePath)))
            {
                throw new ArgumentException("The specified csv file does not exist.", nameof(csvFilePath));
            }

            // Create a new DataTable
            DataTable dataTable = new DataTable();

            // Read the CSV file line by line
            string[] csvLines = File.ReadAllLines(Path.Combine(defaultDirectory, csvFilePath));

            // Add the column headers to the DataTable
            string[] headers = csvLines[0].Split(',');
            foreach (string header in headers)
            {
                dataTable.Columns.Add(header);
            }

            // Add the data rows to the DataTable
            for (int i = 1; i < csvLines.Length; i++)
            {
                string[] fields = csvLines[i].Split(',');
                dataTable.Rows.Add(fields);
            }

            // Bind the DataTable to the DataGridView
            dataGridView.DataSource = dataTable;
        }

        private void ShowImage(string imagePath, PictureBox pictureBox)
        {
            if (!File.Exists(Path.Combine(defaultDirectory, imagePath)))
            {
                throw new ArgumentException("The specified image file does not exist.", nameof(imagePath));
            }

            if (pictureBox.Image != null)
            {
                pictureBox.Image.Dispose();
                pictureBox.Image = null;
            }

            using (Image image = Image.FromFile(Path.Combine(defaultDirectory, imagePath)))
            {
                if (image.PropertyIdList.Contains(0x0112)) // Check if the image has orientation metadata
                {
                    int orientation = (int)image.GetPropertyItem(0x0112).Value[0];
                    switch (orientation)
                    {
                        case 2: // Flip horizontally
                            image.RotateFlip(RotateFlipType.RotateNoneFlipX);
                            break;
                        case 3: // Rotate 180 degrees
                            image.RotateFlip(RotateFlipType.Rotate180FlipNone);
                            break;
                        case 4: // Flip vertically
                            image.RotateFlip(RotateFlipType.RotateNoneFlipY);
                            break;
                        case 5: // Rotate 90 degrees clockwise and flip horizontally
                            image.RotateFlip(RotateFlipType.Rotate90FlipX);
                            break;
                        case 6: // Rotate 90 degrees clockwise
                            image.RotateFlip(RotateFlipType.Rotate90FlipNone);
                            break;
                        case 7: // Rotate 90 degrees clockwise and flip vertically
                            image.RotateFlip(RotateFlipType.Rotate90FlipY);
                            break;
                        case 8: // Rotate 270 degrees clockwise
                            image.RotateFlip(RotateFlipType.Rotate270FlipNone);
                            break;
                        default:
                            break;
                    }
                }

                Invoke(new MethodInvoker(() =>
                {
                    pictureBox.Image = new Bitmap(image);
                    percentageScale(pictureBox);

                    if (pictureBox.Name == "Image_box")
                    {
                        down_scale.Enabled = true;
                        up_scale.Enabled = true;
                        add_template.Enabled = false;
                    }

                    if ((templatePath != null) && (targetImagePath != null))
                    {
                        Match_template.Enabled = true;
                    }
                }));
            }
        }


        private void percentageScale(PictureBox pictureBox)
        {
            if (pictureBox.Name != "Image_box")
            {
                return;
            }

            float originalWidth = pictureBox.Image.Width;
            float originalHeight = pictureBox.Image.Height;
            float aspectRatio = originalWidth / originalHeight;

            float resizedWidth = pictureBox.Width;
            float resizedHeight = pictureBox.Height;

            if (resizedWidth / resizedHeight > aspectRatio)
            {
                resizedWidth = resizedHeight * aspectRatio;
            }
            else
            {
                resizedHeight = resizedWidth / aspectRatio;
            }

            float widthPercentage = resizedWidth / originalWidth * 100;
            float heightPercentage = resizedHeight / originalHeight * 100;

            percentage_scale.Text = $"{(int)Math.Round(widthPercentage)}%";
        }

        private void ResizePictureBox(float percentage)
        {
            float originalWidth = Image_box.Image.Width;
            float originalHeight = Image_box.Image.Height;
            float aspectRatio = originalWidth / originalHeight;

            float resizedWidth = originalWidth * (percentage / 100);
            float resizedHeight = resizedWidth / aspectRatio;

            Image_box.Width = (int)resizedWidth;
            Image_box.Height = (int)resizedHeight;
        }

        private void percentage_scale_TextChanged(object sender, EventArgs e)
        {
            if (float.TryParse(percentage_scale.Text.Replace("%", ""), out float percentage))
            {
                ResizePictureBox(percentage);
            }
        }

        private string get_relativePath(string path, string defaultPaht)
        {
            Uri fullUri = new Uri(path);
            Uri defaultUri = new Uri(defaultPaht);
            string relativePath = Uri.UnescapeDataString(defaultUri.MakeRelativeUri(fullUri).ToString());
            return relativePath;
        }

        private void StartServer()
        {   
            IPAddress ipAddress = IPAddress.Parse(serverIP.Text);
            int port = 48951;
            int port2 = 48952;
            int port3 = 48953;

            // Robot - Winforms - Run CVU algorithm
            serverSocket = new TcpListener(ipAddress, port);
            serverSocket.Start();
            isRunning = true;

            // CVU - Winforms - Get positions of detected objects
            serverSocket2 = new TcpListener(ipAddress, port2);
            serverSocket2.Start();
            isRunning2 = true;

            // Robot - Winforms - Send each position when receiving the request
            serverSocket3 = new TcpListener(ipAddress, port3);
            serverSocket3.Start();
            isRunning3 = true;

            // Start a new thread to accept client connections
            serverThread = new Thread(new ThreadStart(AcceptClients));
            serverThread.Start();

            serverThread2 = new Thread(new ThreadStart(AcceptClients2));
            serverThread2.Start();

            serverThread3 = new Thread(new ThreadStart(AcceptClients3));
            serverThread3.Start();
        }

        private void AcceptClients()
        {
            while (isRunning)
            {
                try
                {
                    TcpClient clientSocket = serverSocket.AcceptTcpClient();
                    Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClient));
                    clientThread.Start(clientSocket);
                }

                catch (SocketException)
                {
                    break;
                }
            }
        }

        private void AcceptClients2()
        {
            while (isRunning2)
            {
                try
                {
                    TcpClient clientSocket = serverSocket2.AcceptTcpClient();
                    Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClient2));
                    clientThread.Start(clientSocket);
                }
                catch (SocketException)
                {
                    break;
                }
            }
        }

        private void AcceptClients3()
        {
            while (isRunning3)
            {
                try
                {
                    TcpClient clientSocket = serverSocket3.AcceptTcpClient();
                    Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClient3));
                    clientThread.Start(clientSocket);
                }
                catch (SocketException)
                {
                    break;
                }
            }
        }

        private void HandleClient(object clientObj)
        {
            TcpClient clientSocket = (TcpClient)clientObj;

            try
            {
                NetworkStream networkStream = clientSocket.GetStream();
                byte[] buffer = new byte[clientSocket.ReceiveBufferSize];

                int bytesRead = networkStream.Read(buffer, 0, clientSocket.ReceiveBufferSize);
                sbyte receivedInteger = (sbyte)buffer[0];

                if (receivedInteger == 100)
                {
                    // Create a new TaskCompletionSource and assign it to matchTemplateCompletionSource
                    matchTemplateCompletionSource = new TaskCompletionSource<bool>();

                    // Invoke the conduct_match_template method on the UI thread
                    string response = null;
                    int numberOfObjects = 0;
                    BeginInvoke(new MethodInvoker(async () =>
                    {
                        stopwatch.Reset();
                        stopwatch.Start();
                        Elasped_time.Text = "...";
                        CVU_status.Text = "Running...";

                        //await conduct_capture_frame();

                        response = await conduct_match_template();

                        try
                        {
                            numberOfObjects = int.Parse(response);
                        }
                        
                        catch
                        {
                            numberOfObjects = 0;
                        }

                        // After the conduct_match_template method is complete, set the task completion source result
                        matchTemplateCompletionSource.SetResult(true);
                    }));

                    // Wait for the task completion source to complete
                    matchTemplateCompletionSource.Task.Wait();

                    byte byteNumberOfObjects = (byte)numberOfObjects;
                    networkStream.WriteByte(byteNumberOfObjects);
                    networkStream.Flush();

                    stopwatch.Stop();
                    TimeSpan elapsedTime = stopwatch.Elapsed;
                    double roundedElapsedTime = Math.Round(elapsedTime.TotalSeconds, 2);
                    string elapsedTimeString = roundedElapsedTime.ToString();

                    BeginInvoke(new MethodInvoker(() =>
                    {
                        Elasped_time.Text = $"{elapsedTimeString} s";

                        string resultImagePath = Path.Combine(output_folder, "output.jpg");
                        string csvPath = Path.Combine(output_folder, "result.csv");

                        try
                        {
                            ShowImage(resultImagePath, Image_box);
                            LoadCsvToDataGridView(csvPath, dataGridView1);
                            CVU_status.Text = "Completed";
                        }
                        catch (Exception)
                        {
                            CVU_status.Text = "No detection found";
                        }
                    }));
                }
            }

            catch (Exception e)
            {
                MessageBox.Show($"{e}");
            }
            finally
            {
                clientSocket.Close();
            }
        }

        private void HandleClient2(object clientObj)
        {
            TcpClient clientSocket = (TcpClient)clientObj;

            try
            {
                byte[] numBytes = new byte[1];
                NetworkStream networkStream = clientSocket.GetStream();
                int bytesRead = networkStream.Read(numBytes, 0, 1);

                if (bytesRead == 0)
                {
                    return;
                }
                int numArrays = numBytes[0];

                lock (sharedData)
                {
                    sharedData.Clear();

                    for (int i = 0; i < numArrays; i++)
                    {
                        // Receive the array of 4 float values (x, y, z, r)
                        byte[] arrayBytes = new byte[16];
                        bytesRead = clientSocket.GetStream().Read(arrayBytes, 0, 16);
                        if (bytesRead == 0)
                        {
                            return;
                        }

                        float[] receivedArray = new float[4];
                        for (int j = 0; j < 4; j++)
                        {
                            if (BitConverter.IsLittleEndian)
                                Array.Reverse(arrayBytes, j * 4, 4);
                            receivedArray[j] = BitConverter.ToSingle(arrayBytes, j * 4);
                        }
                        sharedData.Add(receivedArray);
                    }
                }

                byte response = 100;
                networkStream.WriteByte(response);
                networkStream.Flush();

            }
            catch (Exception e)
            {
                MessageBox.Show($"{e}");
            }
            finally
            {
                clientSocket.Close();
            }
        }

        private void HandleClient3(object clientObj)
        {
            TcpClient clientSocket = (TcpClient)clientObj;
            try
            {
                // Access the shared data
                float[][] dataArray;
                lock (sharedData)
                {
                    dataArray = sharedData.ToArray();
                }

                NetworkStream networkStream = clientSocket.GetStream();
                byte[] buffer = new byte[clientSocket.ReceiveBufferSize];

                int bytesRead = networkStream.Read(buffer, 0, clientSocket.ReceiveBufferSize);
                sbyte receivedIndex = (sbyte)buffer[0];

                float[] data = dataArray[receivedIndex];

                byte[] arrayBytes = new byte[16];
                for (int i = 0; i < 4; i++)
                {
                    byte[] floatBytes = BitConverter.GetBytes(data[i]);
                    if (BitConverter.IsLittleEndian)
                        Array.Reverse(floatBytes);
                    Buffer.BlockCopy(floatBytes, 0, arrayBytes, i * 4, 4);
                }

                networkStream.Write(arrayBytes, 0, arrayBytes.Length);
            }
            catch (Exception e)
            {
                MessageBox.Show($"{e}");
            }
            finally
            {
                clientSocket.Close();
            }
        }


        private void DisconnectServer()
        {
            if (serverStatus.Text == "Connected")
            {
                // Set the flag to stop the server thread
                isRunning = false;
                isRunning2 = false;
                isRunning3 = false;

                // Close the server socket to stop AcceptTcpClient() blocking
                serverSocket.Stop();
                serverSocket2.Stop();
                serverSocket3.Stop();

                // Wait for the server thread to exit gracefully
                serverThread.Join();
                serverThread2.Join();
                serverThread3.Join();
            }
        }

        private void Socket_connect_Click(object sender, EventArgs e)
        {
            StartServer();
            serverStatus.Text = "Connected";
            Socket_connect.Enabled = false;
            Socket_disconnect.Enabled = true;
        }

        private void Socket_disconnect_Click(object sender, EventArgs e)
        {
            DisconnectServer();
            serverStatus.Text = "Disconnected";
            Socket_connect.Enabled = true;
            Socket_disconnect.Enabled = false;
        }

        async Task<string> SendRequest(string url, Dictionary<string, string> formFields)
        {
            using (var client = new HttpClient())
            {
                using (var formData = new MultipartFormDataContent())
                {
                    foreach (var field in formFields)
                    {
                        formData.Add(new StringContent(field.Value), field.Key);
                    }

                    var response = await client.PostAsync(url, formData);

                    response.EnsureSuccessStatusCode();

                    return await response.Content.ReadAsStringAsync();
                }
            }
        }

        private async Task<string> conduct_match_template()
        {
            // Clear the DataGridView before assigning the new data source
            dataGridView1.DataSource = null;
            dataGridView1.Rows.Clear();
            dataGridView1.Columns.Clear();

            var formFields = new Dictionary<string, string>
            {
                {"api_folder", defaultDirectory},
                {"img_path", targetImagePath},
                {"template_path", templatePath},
                {"threshold", Similarity_score.Text},
                {"overlap", Overlap.Text},
                {"method", Method_similarity.Text},
                {"min_modify", Min_modify.Text},
                {"max_modify", Max_modify.Text},
                {"conf_score", conf_score.Text},
                {"img_size", img_size.Text},
                {"server_ip", serverIP.Text},
                {"output_folder", output_folder}
            };

            var response = await SendRequest("http://127.0.0.1:5000/my_cvu_api", formFields);

            return response;
        }

        private async void Match_template_Click(object sender, EventArgs e)
        {
            stopwatch.Reset();
            stopwatch.Start();
            Elasped_time.Text = "...";
            CVU_status.Text = "Running...";

            _ = await conduct_match_template();

            stopwatch.Stop();
            TimeSpan elapsedTime = stopwatch.Elapsed;
            double roundedElapsedTime = Math.Round(elapsedTime.TotalSeconds, 2);
            string elapsedTimeString = roundedElapsedTime.ToString();

            Elasped_time.Text = $"{elapsedTimeString} s";

            string resultImagePath = Path.Combine(output_folder, "output.jpg");
            string csvPath = Path.Combine(output_folder, "result.csv");

            try
            {
                ShowImage(resultImagePath, Image_box);
                LoadCsvToDataGridView(csvPath, dataGridView1);
                CVU_status.Text = "Completed";
            }
            catch (Exception)
            {
                CVU_status.Text = "No detection found";
            }
        }

        private async Task conduct_capture_frame()
        {
            string cameraPath = Path.Combine(stream_folder, "input_image.jpg");

            try
            {
                await captureFrame();
            }
            catch (Exception e)
            {
                MessageBox.Show($"{e}");
            }

            targetImagePath = cameraPath;
        }

        private async void Cam_capture_Click(object sender, EventArgs e)
        {
            await conduct_capture_frame();

            string cameraPath = Path.Combine(stream_folder, "input_image.jpg");
            Match_template.Enabled = true;
            try
            {
                ShowImage(cameraPath, Image_box);
            }
            catch (Exception)
            {
                MessageBox.Show("No connection with camera");
            }
        }

        private void Image_box_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                isSelecting = true;
                startPoint = e.Location;
            }
        }

        private void Image_box_MouseUp(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                isSelecting = false;
                isReshape = false;

                // update selectedRect with the selected region's rectangle
                selectedRect = new Rectangle(Math.Min(rect.Left, rect.Right),
                                             Math.Min(rect.Top, rect.Bottom),
                                             Math.Abs(rect.Width),
                                             Math.Abs(rect.Height));

                add_template.Enabled = true;
            }
        }

        private void Image_box_MouseMove(object sender, MouseEventArgs e)
        {
            if (isSelecting)
            {
                int x = Math.Min(startPoint.X, e.Location.X);
                int y = Math.Min(startPoint.Y, e.Location.Y);
                int width = Math.Abs(startPoint.X - e.Location.X);
                int height = Math.Abs(startPoint.Y - e.Location.Y);

                rect = new Rectangle(x, y, width, height);
                Image_box.Invalidate();
            }
        }

        private void Image_box_Paint(object sender, PaintEventArgs e)
        {
            if ((isSelecting || isReshape) && rect.Width > 0 && rect.Height > 0)
            {
                using (Pen pen = new Pen(Color.Green, 2))
                {
                    e.Graphics.DrawRectangle(pen, rect);

                    int rectX = rect.X;
                    int rectY = rect.Y;
                    int rectWidth = rect.Width;
                    int rectHeight = rect.Height;

                    // Draw small rectangles at each corner of the rect
                    e.Graphics.FillRectangle(Brushes.Green, rectX - cornerSize + 1, rectY - cornerSize + 1, cornerSize * 2 - 2, cornerSize * 2 - 2);
                    e.Graphics.FillRectangle(Brushes.Green, rectX + rectWidth - cornerSize + 1, rectY - cornerSize + 1, cornerSize * 2 - 2, cornerSize * 2 - 2);
                    e.Graphics.FillRectangle(Brushes.Green, rectX - cornerSize + 1, rectY + rectHeight - cornerSize + 1, cornerSize * 2 - 2, cornerSize * 2 - 2);
                    e.Graphics.FillRectangle(Brushes.Green, rectX + rectWidth - cornerSize + 1, rectY + rectHeight - cornerSize + 1, cornerSize * 2 - 2, cornerSize * 2 - 2);
                }
            }
        }

        private void add_template_Click(object sender, EventArgs e)
        {
            string streamTemplatePath = Path.Combine(template_folder, "template.jpg");

            if (selectedRect.Width > 0 && selectedRect.Height > 0)
            {
                Bitmap bitmap = new Bitmap(Image_box.ClientSize.Width, Image_box.ClientSize.Height);
                Image_box.DrawToBitmap(bitmap, Image_box.ClientRectangle);

                Bitmap croppedBitmap = bitmap.Clone(selectedRect, bitmap.PixelFormat);

                if (!Directory.Exists(template_folder))
                {
                    Directory.CreateDirectory(template_folder);
                }

                croppedBitmap.Save(streamTemplatePath, ImageFormat.Jpeg);
            }

            try
            {
                ShowImage(streamTemplatePath, Template_box);
            }
            catch (Exception)
            {
                MessageBox.Show("Please select a region of interest first");
            }

            templatePath = streamTemplatePath;
        }

        private void updateScrollBarPositions()
        {
            // Calculate the difference between the old and new size of the picture box
            int deltaX = Image_box.Width - hScrollBar1.Maximum;
            int deltaY = Image_box.Height - vScrollBar1.Maximum;

            // Check if the picture box is smaller than the panel and adjust the scroll bar values accordingly
            if (deltaX < 0)
            {
                hScrollBar1.Value = 0;
                deltaX = 0;
            }
            if (deltaY < 0)
            {
                vScrollBar1.Value = 0;
                deltaY = 0;
            }

            // Calculate the new position of the scroll bars based on the difference
            int newHValue = Math.Max(-Image_box.Location.X, 0);
            int newVValue = Math.Max(-Image_box.Location.Y, 0);

            // Update the scrollbars' maximum values to reflect the new size of the picturebox
            hScrollBar1.Maximum = Math.Max(Image_box.Width - panel13.Width, 0);
            vScrollBar1.Maximum = Math.Max(Image_box.Height - panel13.Height, 0);

            // Make sure the scrollbars' values are still within their maximum range
            hScrollBar1.Value = Math.Min(newHValue, hScrollBar1.Maximum);
            vScrollBar1.Value = Math.Min(newVValue, vScrollBar1.Maximum);

            // Update the position of the picturebox based on the scrollbar values
            Image_box.Location = new Point(Math.Max(-hScrollBar1.Value, 6), Math.Max(-vScrollBar1.Value, 21));
        }

        private void vScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            Image_box.Top = -e.NewValue;
        }

        private void hScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            Image_box.Left = -e.NewValue;
        }

        private void Image_box_Resize(object sender, EventArgs e)
        {
            Image_box.SizeMode = PictureBoxSizeMode.Zoom;
            updateScrollBarPositions();
        }

        private void hScrollBar1_ValueChanged(object sender, EventArgs e)
        {
            Image_box.Left = -hScrollBar1.Value;
        }

        private void vScrollBar1_ValueChanged(object sender, EventArgs e)
        {
            Image_box.Top = -vScrollBar1.Value;
        }

        private void down_scale_MouseDown(object sender, MouseEventArgs e)
        {

            isResizing = true;
            int scaleFactor = Convert.ToInt32(Scale_ratio.Text);
            while (isResizing)
            {
                float aspectRatio = (float)Image_box.Image.Width / (float)Image_box.Image.Height;
                int newWidth = Image_box.Width - (int)(scaleFactor * 1);
                int newHeight = (int)(newWidth / aspectRatio);

                Point oldCenter = new Point(Image_box.Location.X + Image_box.Width / 2,
                                             Image_box.Location.Y + Image_box.Height / 2);

                Image_box.Size = new Size(newWidth, newHeight);

                Point newCenter = new Point(oldCenter.X + (Image_box.Width - newWidth) / 2,
                                             oldCenter.Y + (Image_box.Height - newHeight) / 2);

                Image_box.Location = new Point(newCenter.X - Image_box.Width / 2,
                                                 newCenter.Y - Image_box.Height / 2);

                percentageScale(Image_box);
                updateScrollBarPositions();
                Application.DoEvents();
            }
        }

        private void down_scale_MouseUp(object sender, MouseEventArgs e)
        {
            isResizing = false;
        }

        private void up_scale_MouseDown(object sender, MouseEventArgs e)
        {
            isResizing = true;
            int scaleFactor = Convert.ToInt32(Scale_ratio.Text);
            while (isResizing)
            {
                float aspectRatio = (float)Image_box.Image.Width / (float)Image_box.Image.Height;
                int newWidth = Image_box.Width + (int)(scaleFactor * 1);
                int newHeight = (int)(newWidth / aspectRatio);

                Point oldCenter = new Point(Image_box.Location.X + Image_box.Width / 2,
                                             Image_box.Location.Y + Image_box.Height / 2);

                Image_box.Size = new Size(newWidth, newHeight);

                Point newCenter = new Point(oldCenter.X - (newWidth - Image_box.Width) / 2,
                                             oldCenter.Y - (newHeight - Image_box.Height) / 2);

                Image_box.Location = new Point(newCenter.X - Image_box.Width / 2,
                                                 newCenter.Y - Image_box.Height / 2);

                percentageScale(Image_box);
                updateScrollBarPositions();
                Application.DoEvents();
            }
        }

        private void up_scale_MouseUp(object sender, MouseEventArgs e)
        {
            isResizing = false;
        }
    }
}
