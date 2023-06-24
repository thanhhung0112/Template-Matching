using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;


namespace NeptuneC_Interface
{
    //////////////////////////////////////////////////////////////////////////
    public enum ENeptuneError
    {
        NEPTUNE_ERR_Fail                    = -1,
        NEPTUNE_ERR_Success                 = 0,
        NEPTUNE_ERR_AlreadyInitialized      = -100,
        NEPTUNE_ERR_APINotInitialized       = -101,
        NEPTUNE_ERR_NotInitialized          = -102,
        NEPTUNE_ERR_GC                      = -103,
        NEPTUNE_ERR_TimeOut                 = -104,
        NEPTUNE_ERR_NotSupportedFunc        = -105,
        NEPTUNE_ERR_OpenXML                 = -106,
        NEPTUNE_ERR_InvalidValue            = -107,
        NEPTUNE_ERR_EventChannel            = -108,
        NEPTUNE_ERR_NotReady                = -109,
        NEPTUNE_ERR_PacketResend            = -110,
        NEPTUNE_ERR_InvalidFeatureRange     = -111,
        NEPTUNE_ERR_TLInterface             = -112,
        NEPTUNE_ERR_TLDevOpen               = -113,
        NEPTUNE_ERR_TLDevPort               = -114,
        NEPTUNE_ERR_TLDevURL                = -115,
        NEPTUNE_ERR_GrabTimeout             = -116,
        NEPTUNE_ERR_DeviceNotExist          = -117,
        NEPTUNE_ERR_TLInitFail              = -200,
        NEPTUNE_ERR_NoInterface             = -201,
        NEPTUNE_ERR_DeviceCheck             = -202,
        NEPTUNE_ERR_InvalidParameter        = -203,
        NEPTUNE_ERR_NotSupport              = -204,
        NEPTUNE_ERR_AccessDenied            = -205,
        NEPTUNE_ERR_InvalidAddress          = -206,
        NEPTUNE_ERR_InvalidArraySize        = -207,
        NEPTUNE_ERR_Interface               = -208,
        NEPTUNE_ERR_DeviceInfo              = -209,
        NEPTUNE_ERR_MemoryAlloc             = -210,
        NEPTUNE_ERR_DeviceOpen              = -211,
        NEPTUNE_ERR_DevicePort              = -212,
        NEPTUNE_ERR_DeviceURL               = -213,
        NEPTUNE_ERR_DeviceWrite             = -214,
        NEPTUNE_ERR_DeviceXML               = -215,
        NEPTUNE_ERR_DeviceHeartbeat         = -216,
        NEPTUNE_ERR_DeviceClose             = -217,
        NEPTUNE_ERR_DeviceStream            = -218,
        NEPTUNE_ERR_DeviceNotStreaming      = -219,
        NEPTUNE_ERR_DeviceStreaming         = -220,
        NEPTUNE_ERR_InvalidXMLNode          = -300,
        NEPTUNE_ERR_StreamCount             = -303,
        NEPTUNE_ERR_AccessTimeOut           = -304,
        NEPTUNE_ERR_OutOfRange              = -305,
        NEPTUNE_ERR_InvalidChannel          = -306,
        NEPTUNE_ERR_InvalidBuffer           = -307,
        NEPTUNE_ERR_FileAccessError         = -400,
        NEPTUNE_ERR_GrabFrameDropped        = -450
    };

    public enum ENeptuneBoolean
    {
        NEPTUNE_BOOL_FALSE                  = 0,
        NEPTUNE_BOOL_TRUE                   = 1
    };

    public enum ENeptuneEffect
    {
        NEPTUNE_EFFECT_NONE                 = 0,
        NEPTUNE_EFFECT_FLIP                 = 0x01,
        NEPTUNE_EFFECT_MIRROR               = 0x02,
        NEPTUNE_EFFECT_NEGATIVE             = 0x04
    };

    public enum ENeptuneAutoMode
    {
        NEPTUNE_AUTO_OFF                    = 0,
        NEPTUNE_AUTO_ONCE                   = 1,
        NEPTUNE_AUTO_CONTINUOUS             = 2 
    };

    public enum ENeptunePixelFormat
    {
        Unknown_PixelFormat                 = -1,

        // 1394 Camera pixel format list.
        Format0_320x240_YUV422              = 0,
        Format0_640x480_YUV411              = 1,
        Format0_640x480_YUV422              = 2,
        Format0_640x480_Mono8               = 3,
        Format0_640x480_Mono16              = 4,
        Format1_800x600_YUV422              = 5,
        Format1_800x600_Mono8               = 6,
        Format1_1024x768_YUV422             = 7,
        Format1_1024x768_Mono8              = 8,
        Format1_800x600_Mono16              = 9,
        Format1_1024x768_Mono16             = 10,

        Format2_1280x960_YUV422             = 11,
        Format2_1280x960_Mono8              = 12,
        Format2_1600x1200_YUV422            = 13,
        Format2_1600x1200_Mono8             = 14,
        Format2_1280x960_Mono16             = 15,
        Format2_1600x1200_Mono16            = 16,

        Format7_Mode0_Mono8                 = 17,
        Format7_Mode0_YUV411                = 18,
        Format7_Mode0_YUV422                = 19,
        Format7_Mode0_Mono16                = 20,
        Format7_Mode0_Raw8                  = 21,
        Format7_Mode0_Raw16                 = 22,
        Format7_Mode0_Mono12                = 23,
        Format7_Mode0_Raw12                 = 24,

        Format7_Mode1_Mono8                 = 25,
        Format7_Mode1_YUV411                = 26,
        Format7_Mode1_YUV422                = 27,
        Format7_Mode1_Mono16                = 28,
        Format7_Mode1_Raw8                  = 29,
        Format7_Mode1_Raw16                 = 30,
        Format7_Mode1_Mono12                = 31,
        Format7_Mode1_Raw12                 = 32,

        Format7_Mode2_Mono8                 = 33,
        Format7_Mode2_YUV411                = 34,
        Format7_Mode2_YUV422                = 35,
        Format7_Mode2_Mono16                = 36,
        Format7_Mode2_Raw8                  = 37,
        Format7_Mode2_Raw16                 = 38,
        Format7_Mode2_Mono12                = 39,
        Format7_Mode2_Raw12                 = 40,

        // GigE/USB3 Camera pixel format list.
        Mono8                               = 101,
        Mono10                              = 102,
        Mono12                              = 103,
        Mono16                              = 104,
        BayerGR8                            = 105,
        BayerGR10                           = 106,
        BayerGR12                           = 107,
        YUV411Packed                        = 108,
        YUV422Packed                        = 109,
        YUV422_8                            = 110,
        BayerRG8                            = 111,
        BayerRG12                           = 112,
        BayerGB8                            = 113,
        BayerGB12                           = 114,
        BayerBG8                            = 115,
        BayerBG12                           = 116,
        Profile32                           = 117
    };

    public enum ENeptunePixelType
    {
        NEPTUNE_PIXEL_MONO                  = 1,
        NEPTUNE_PIXEL_BAYER                 = 2,
        NEPTUNE_PIXEL_RGB                   = 3,
        NEPTUNE_PIXEL_YUV                   = 4,
        NEPTUNE_PIXEL_RGBPLANAR             = 5,
        NEPTUNE_PIXEL_YUV_8                 = 6,
        NEPTUNE_PIXEL_PROFILE32             = 7
    };

    public enum ENeptuneFrameRate
    {
        FPS_UNKNOWN                         = -1,
        FPS_1_875                           = 0,
        FPS_3_75                            = 1,
        FPS_7_5                             = 2,
        FPS_15                              = 3,
        FPS_30                              = 4,
        FPS_60                              = 5,
        FPS_120                             = 6,
        FPS_240                             = 7,
        FPS_VALUE                           = 20
    };

    public enum ENeptuneBayerLayout
    {
        NEPTUNE_BAYER_GB_RG                 = 0,
        NEPTUNE_BAYER_BG_GR                 = 1,
        NEPTUNE_BAYER_RG_GB                 = 2,
        NEPTUNE_BAYER_GR_BG                 = 3
    };

    public enum ENeptuneBayerMethod
    {
        NEPTUNE_BAYER_METHOD_NONE           = 0,
        NEPTUNE_BAYER_METHOD_BILINEAR       = 1,
        NEPTUNE_BAYER_METHOD_HQ             = 2,
        NEPTUNE_BAYER_METHOD_NEAREST        = 3
    };

    public enum ENeptuneAcquisitionMode
    {
        NEPTUNE_ACQ_CONTINUOUS              = 0,
        NEPTUNE_ACQ_MULTIFRAME              = 1,
        NEPTUNE_ACQ_SINGLEFRAME             = 2
    };

    public enum ENeptuneImageFormat
    {
	    NEPTUNE_IMAGE_FORMAT_UNKNOWN	    = -1,
	    NEPTUNE_IMAGE_FORMAT_BMP	    	= 0,
	    NEPTUNE_IMAGE_FORMAT_JPG	    	= 1,
	    NEPTUNE_IMAGE_FORMAT_TIF	    	= 2
    };

    public enum ENeptuneGrabFormat
    {
	    NEPTUNE_GRAB_RAW                	= 0,
	    NEPTUNE_GRAB_RGB                	= 1,
	    NEPTUNE_GRAB_RGB32              	= 2
    };

    public enum ENeptuneDeviceChangeState
    {
	    NEPTUNE_DEVICE_ADDED	           	= 0,
	    NEPTUNE_DEVICE_REMOVED	        	= 1
    };

    public enum ENeptuneRotationAngle
    {
	    NEPTUNE_ROTATE_0		            = 0,
	    NEPTUNE_ROTATE_90	            	= 1,
	    NEPTUNE_ROTATE_180	            	= 2,
	    NEPTUNE_ROTATE_270		            = 3
    };

    public enum ENeptuneCameraListOpt
    {
        NEPTUNE_CAMERALISTOPT_ONLYIMI       = 0,
        NEPTUNE_CAMERALISTOPT_ALL           = 1
    };

    public enum ENeptuneDisplayOption
    {
        NEPTUNE_DISPLAY_OPTION_FIT          = 0,
        NEPTUNE_DISPLAY_OPTION_ORIGINAL_CENTER = 1
    };

    public enum ENeptune1394Foramt
    {
        FORMAT_0 = 0,
        FORMAT_1 = 1,
        FORMAT_2 = 2,
        FORMAT_7 = 7
    };

    public enum ENeptuneDevType
    {
        NEPTUNE_DEV_TYPE_UNKNOWN = -1,
        NEPTUNE_DEV_TYPE_1394 = 0,
        NEPTUNE_DEV_TYPE_USB3 = 1,
        NEPTUNE_DEV_TYPE_GIGE = 2
    };

    public enum ENeptuneDevAccess
    {
        NEPTUNE_DEV_ACCESS_UNKNOWN = -1,
        NEPTUNE_DEV_ACCESS_EXCLUSIVE = 0,
        NEPTUNE_DEV_ACCESS_CONTROL = 1,
        NEPTUNE_DEV_ACCESS_MONITOR = 2
    };

    public enum ENeptuneFeature
    {
        NEPTUNE_FEATURE_GAMMA = 0,
        NEPTUNE_FEATURE_GAIN = 1,
        NEPTUNE_FEATURE_RGAIN = 2,
        NEPTUNE_FEATURE_GGAIN = 3,
        NEPTUNE_FEATURE_BGAIN = 4,
        NEPTUNE_FEATURE_BLACKLEVEL = 5,
        NEPTUNE_FEATURE_SHARPNESS = 6,
        NEPTUNE_FEATURE_SATURATION = 7,
        NEPTUNE_FEATURE_AUTOEXPOSURE = 8,
        NEPTUNE_FEATURE_SHUTTER = 9,
        NEPTUNE_FEATURE_HUE = 10,
        NEPTUNE_FEATURE_PAN = 11,
        NEPTUNE_FEATURE_TILT = 12,
        NEPTUNE_FEATURE_OPTFILTER = 13,
        NEPTUNE_FEATURE_AUTOSHUTTER_MIN = 14,
        NEPTUNE_FEATURE_AUTOSHUTTER_MAX = 15,
        NEPTUNE_FEATURE_AUTOGAIN_MIN = 16,
        NEPTUNE_FEATURE_AUTOGAIN_MAX = 17,
        NEPTUNE_FEATURE_TRIGNOISEFILTER = 18,
        NEPTUNE_FEATURE_BRIGHTLEVELIRIS = 19,
        NEPTUNE_FEATURE_SNOWNOISEREMOVE = 20,
        NEPTUNE_FEATURE_WATCHDOG = 21,
        NEPTUNE_FEATURE_WHITEBALANCE = 22,
        NEPTUNE_FEATURE_CONTRAST = 23,
        NEPTUNE_FEATURE_LCD_BLUE_GAIN = 24,
        NEPTUNE_FEATURE_LCD_RED_GAIN = 25
    };

    public enum ENeptuneUserSet
    {
        NEPTUNE_USERSET_DEFAULT = 0,
        NEPTUNE_USERSET_1 = 1,
        NEPTUNE_USERSET_2 = 2,
        NEPTUNE_USERSET_3 = 3,
        NEPTUNE_USERSET_4 = 4,
        NEPTUNE_USERSET_5 = 5,
        NEPTUNE_USERSET_6 = 6,
        NEPTUNE_USERSET_7 = 7,
        NEPTUNE_USERSET_8 = 8,
        NEPTUNE_USERSET_9 = 9,
        NEPTUNE_USERSET_10 = 10,
        NEPTUNE_USERSET_11 = 11,
        NEPTUNE_USERSET_12 = 12,
        NEPTUNE_USERSET_13 = 13,
        NEPTUNE_USERSET_14 = 14,
        NEPTUNE_USERSET_15 = 15
    };

    public enum ENeptuneUserSetCommand
    {
        NEPTUNE_USERSET_CMD_LOAD = 0,
        NEPTUNE_USERSET_CMD_SAVE = 1
    };

    public enum ENeptuneAutoIrisMode
    {
        NEPTUNE_AUTOIRIS_MODE_MANUAL = 0,
        NEPTUNE_AUTOIRIS_MODE_AUTO = 1
    };

    public enum ENeptuneSIOParity
    {
        NEPTUNE_SIO_PARITY_NONE = 0,
        NEPTUNE_SIO_PARITY_ODD = 1,
        NEPTUNE_SIO_PARITY_EVEN = 2
    };

    public enum ENeptuneAutoAreaSelect
    {
        NEPTUNE_AUTOAREA_SELECT_AE = 0,
        NEPTUNE_AUTOAREA_SELECT_AWB = 1,
        NEPTUNE_AUTOAREA_SELECT_AF = 2
    };

    public enum ENeptuneAutoAreaSize
    {
        NEPTUNE_AUTOAREA_SIZE_SELECTED = 0,
        NEPTUNE_AUTOAREA_SIZE_FULL = 1
    };

    public enum ENeptuneAFMode
    {
        NEPTUNE_AF_ORIGIN = 0,
        NEPTUNE_AF_ONEPUSH = 1,
        NEPTUNE_AF_STEP_FORWARD = 2,
        NEPTUNE_AF_STEP_BACKWARD = 3
    };

    public enum ENeptuneTriggerSource
    {
        NEPTUNE_TRIGGER_SOURCE_LINE1 = 0,
        NEPTUNE_TRIGGER_SOURCE_SW = 7
    };

    public enum ENeptuneTriggerMode
    {
        NEPTUNE_TRIGGER_MODE_0 = 0,
        NEPTUNE_TRIGGER_MODE_1,
        NEPTUNE_TRIGGER_MODE_2,
        NEPTUNE_TRIGGER_MODE_3,
        NEPTUNE_TRIGGER_MODE_4,
        NEPTUNE_TRIGGER_MODE_5,
        NEPTUNE_TRIGGER_MODE_6,
        NEPTUNE_TRIGGER_MODE_7,
        NEPTUNE_TRIGGER_MODE_8,
        NEPTUNE_TRIGGER_MODE_9,
        NEPTUNE_TRIGGER_MODE_10,
        NEPTUNE_TRIGGER_MODE_11,
        NEPTUNE_TRIGGER_MODE_12,
        NEPTUNE_TRIGGER_MODE_13,
        NEPTUNE_TRIGGER_MODE_14,
        NEPTUNE_TRIGGER_MODE_15
    };

    public enum ENeptuneStrobe
    {
        NEPTUNE_STROBE0 = 0,
        NEPTUNE_STROBE1 = 1,
        NEPTUNE_STROBE2 = 2,
        NEPTUNE_STROBE3 = 3,
        NEPTUNE_STROBE4 = 4
    };

    public enum ENeptunePolarity
    {
        NEPTUNE_POLARITY_RISINGEDGE = 0,
        NEPTUNE_POLARITY_FALLINGEDGE = 1,
        NEPTUNE_POLARITY_ANYEDGE = 2,
        NEPTUNE_POLARITY_LEVELHIGH = 3,
        NEPTUNE_POLARITY_LEVELLOW = 4
    };

    public enum ENeptuneNodeType
    {
        NEPTUNE_NODE_TYPE_UKNOWN = -1,
        NEPTUNE_NODE_TYPE_CATEGORY = 0,
        NEPTUNE_NODE_TYPE_COMMAND = 1,
        NEPTUNE_NODE_TYPE_RAW = 2,
        NEPTUNE_NODE_TYPE_STRING = 3,
        NEPTUNE_NODE_TYPE_ENUM = 4,
        NEPTUNE_NODE_TYPE_INT = 5,
        NEPTUNE_NODE_TYPE_FLOAT = 6,
        NEPTUNE_NODE_TYPE_BOOLEAN = 7
    };

    public enum ENeptuneNodeAccessMode
    {
        NEPTUNE_NODE_ACCESSMODE_NI = 0,
        NEPTUNE_NODE_ACCESSMODE_NA = 1,
        NEPTUNE_NODE_ACCESSMODE_WO = 2,
        NEPTUNE_NODE_ACCESSMODE_RO = 3,
        NEPTUNE_NODE_ACCESSMODE_RW = 4,
        NEPTUNE_NODE_ACCESSMODE_UNDEFINED = 5
    };

    public enum ENeptuneNodeVisibility
    {
        NEPTUNE_NODE_VISIBLE_UNKNOWN = -1,
        NEPTUNE_NODE_VISIBLE_BEGINNER = 0,
        NEPTUNE_NODE_VISIBLE_EXPERT = 1,
        NEPTUNE_NODE_VISIBLE_GURU = 2
    };

    public enum ENeptuneGPIO
    {
        NEPTUNE_GPIO_LINE0 = 0,
        NEPTUNE_GPIO_LINE1
    };

    public enum ENeptuneGPIOSource
    {
        NEPTUNE_GPIO_SOURCE_STROBE = 0,
        NEPTUNE_GPIO_SOURCE_USER
    };

    public enum ENeptuneGPIOValue
    {
        NEPTUNE_GPIO_VALUE_LOW = 0,
        NEPTUNE_GPIO_VALUE_HIGH
    };


    //////////////////////////////////////////////////////////////////////////
    [StructLayout(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
    public struct NEPTUNE_CAM_INFO
    {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strVendor;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strModel;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strSerial;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strUserID;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strIP;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public String strMAC;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strSubnet;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strGateway;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strCamID;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_IMAGE_SIZE
    {
	    public Int32 nStartX;
	    public Int32 nStartY;
	    public Int32 nSizeX;
	    public Int32 nSizeY;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_IMAGE
    {
        public UInt32 uiWidth;
        public UInt32 uiHeight;
        public UInt32 uiBitDepth;
        public IntPtr pData;
        public UInt32 uiSize;
        public UInt32 uiIndex;
        public UInt64 uiTimestamp;
        public Byte bFrameValid;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_FEATURE
    {
        public ENeptuneBoolean bSupport;
        public ENeptuneBoolean bOnOff;
        public Byte SupportAutoModes;
        public ENeptuneAutoMode AutoMode;
        public Int32 Min;
        public Int32 Max;
        public Int32 Inc;
        public Int32 Value;
        public ENeptuneNodeAccessMode ValueAccessMode;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_PACKAGE_FEATURE
    {
        public UInt32 Gain;
        public UInt32 Sharpness;
        public UInt32 Shutter;
        public UInt32 BlackLevel;
        public UInt32 Contrast;
        public UInt32 Gamma;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_USERSET
    {
        public UInt16 SupportUserSet;
        public ENeptuneUserSet UserSetIndex;
        public ENeptuneUserSetCommand Command;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_POINT
    {
        public UInt32 x;
        public UInt32 y;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_KNEE_LUT
    {
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)]
        public NEPTUNE_POINT[] Points;
        public ENeptuneBoolean bEnable;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_USER_LUT
    {
        public UInt16 SupportLUT;
        public UInt16 LUTIndex;
        public ENeptuneBoolean bEnable;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4096)]
        public UInt16[] Data;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_SIO_PROPERTY
    {
        public ENeptuneBoolean bEnable;
        public UInt32 Baudrate;
        public ENeptuneSIOParity Parity;
        public UInt32 DataBit;
        public UInt32 StopBit;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
    public struct NEPTUNE_SIO
    {
        public UInt32 TextCount;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)]
        public String strText;
        public UInt32 TimeOut;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_AUTOAREA
    {
        public ENeptuneBoolean OnOff;
        public ENeptuneAutoAreaSize SizeControl;
        public NEPTUNE_IMAGE_SIZE AreaSize;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_TRIGGER_INFO
    {
        public ENeptuneBoolean bSupport;
        public UInt16 nModeFlag;
        public UInt16 nSourceFlag;
        public UInt16 nPolarityFlag;
        public UInt16 nParamMin;
        public UInt16 nParamMax;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_TRIGGER
    {
        public ENeptuneTriggerSource Source;
        public ENeptuneTriggerMode Mode;
        public ENeptunePolarity Polarity;
        public ENeptuneBoolean OnOff;
        public UInt16 nParam;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_TRIGGER_PARAM
    {
        public UInt32 nFrameOrder;
        public UInt32 nIncrement;
        public UInt32 nGainValue;
        public UInt32 nShutterValue;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_TRIGGER_TABLE
    {
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 255)]
        public NEPTUNE_TRIGGER_PARAM[] Param;
        public UInt32 Index;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_STROBE_INFO
    {
        public ENeptuneBoolean bSupport;
        public UInt16 nStrobeFlag;
        public UInt16 nPolarityFlag;
        public UInt16 nDurationMin;
        public UInt16 nDurationMax;
        public UInt16 nDelayMin;
        public UInt16 nDelayMax;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_STROBE
    {
        public ENeptuneBoolean OnOff;
        public ENeptuneStrobe Strobe;
        public UInt16 nDuration;
        public UInt16 nDelay;
        public ENeptunePolarity Polarity;
    }

    [StructLayoutAttribute(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
    public struct NEPTUNE_XML_NODE_STRING
    {
        [MarshalAsAttribute(UnmanagedType.ByValTStr, SizeConst = 256)]
        public String nodeString;

        public override String ToString()
        {
            return nodeString;
        }
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
    public struct NEPTUNE_XML_NODE_LIST
    {
	    public UInt32 nCount;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 128)]
        public NEPTUNE_XML_NODE_STRING[] pstrList;

        public static NEPTUNE_XML_NODE_LIST Create()
        {
            NEPTUNE_XML_NODE_LIST ret = new NEPTUNE_XML_NODE_LIST();
            ret.pstrList = new NEPTUNE_XML_NODE_STRING[128];
            return ret;
        }
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
    public struct NEPTUNE_XML_ENUM_LIST
    {
	    public UInt32 nCount;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 64)]
        public NEPTUNE_XML_NODE_STRING[] pstrList;
	    public UInt32 nIndex;

        public static NEPTUNE_XML_ENUM_LIST Create()
        {
            NEPTUNE_XML_ENUM_LIST ret = new NEPTUNE_XML_ENUM_LIST();
            ret.pstrList = new NEPTUNE_XML_NODE_STRING[64];
            return ret;
        }
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
    public struct NEPTUNE_XML_NODE_INFO
    {
	    public ENeptuneNodeType Type;
	    public ENeptuneNodeAccessMode AccessMode;
	    public ENeptuneNodeVisibility Visibility;
	    public bool bHasChild;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
	    public String strDisplayName;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strTooltip;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 512)]
        public String strDescription;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_XML_INT_VALUE_INFO
    {
        public Int64 nValue;
        public Int64 nMin;
        public Int64 nMax;
        public Int64 nInc;
        public ENeptuneNodeAccessMode AccessMode;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_XML_FLOAT_VALUE_INFO
    {
        public Double dValue;
        public Double dMin;
        public Double dMax;
        public Double dInc;
        public ENeptuneNodeAccessMode AccessMode;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct NEPTUNE_GPIO
    {
        public ENeptuneGPIO Gpio;
        public ENeptuneGPIOSource Source;
        public ENeptuneGPIOValue Value;
    }
    

    //////////////////////////////////////////////////////////////////////////
    // device check callback
    public delegate void NeptuneCDevCheckCallback(ENeptuneDeviceChangeState emState, IntPtr pContext);

    // camera unplug callback
    public delegate void NeptuneCUnplugCallback(IntPtr pContext);

    // image received callback
    public delegate void NeptuneCFrameCallback(ref NEPTUNE_IMAGE stImage, IntPtr pContext);

    // frame drop callback
    public delegate void NeptuneCFrameDropCallback(IntPtr pContext);

    // receive frame timeout callback
    public delegate void NeptuneCRecvTimeoutCallback(IntPtr pContext);

    //////////////////////////////////////////////////////////////////////////
    class NeptuneC
    {
        const String strFileName = "NeptuneC_MD_VC141.dll";

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcInit();

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcUninit();

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetCameraCount(ref UInt32 puiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetCameraInfo([Out] NEPTUNE_CAM_INFO[] pCameraInfo, UInt32 uiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcOpen(String pszCameraID, ref IntPtr phCameraHandle, ENeptuneDevAccess emAccessFlag);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcClose(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetCameraType(IntPtr hCameraHandle, ref ENeptuneDevType pemDevType);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetPixelFormatList(IntPtr hCameraHandle, [Out] ENeptunePixelFormat[] pemPixelFmtList, ref UInt32 puiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetPixelFormatString(IntPtr hCameraHandle, ENeptunePixelFormat emPixelFmt, [Out] char[] pszBuffer, UInt32 uiBufSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetPixelFormat(IntPtr hCameraHandle, ref ENeptunePixelFormat pemPixelFmt);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetPixelFormat(IntPtr hCameraHandle, ENeptunePixelFormat emPixelFmt);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetFrameRateList(IntPtr hCameraHandle, [Out] ENeptuneFrameRate[] pemFPSList, ref UInt32 puiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetFrameRateString(IntPtr hCameraHandle, ENeptuneFrameRate emFPS, [Out] char[] pszBuffer, UInt32 uiBufSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetFrameRate(IntPtr hCameraHandle, ref ENeptuneFrameRate pemFPS, ref Double pdbFPS);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetFrameRate(IntPtr hCameraHandle, ENeptuneFrameRate emFPS, Double dbFPS);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetReceiveFrameRate(IntPtr hCameraHandle, ref float pfRecvFPS);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetMaxImageSize(IntPtr hCameraHandle, ref NEPTUNE_IMAGE_SIZE pImageSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetImageSize(IntPtr hCameraHandle, ref NEPTUNE_IMAGE_SIZE pImageSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetImageSize(IntPtr hCameraHandle, NEPTUNE_IMAGE_SIZE stImageSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetAcquisition(IntPtr hCameraHandle, ref ENeptuneBoolean pemState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAcquisition(IntPtr hCameraHandle, ENeptuneBoolean emState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetAcquisitionMode(IntPtr hCameraHandle, ref ENeptuneAcquisitionMode pemAcqMode, ref UInt32 puiFrames);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAcquisitionMode(IntPtr hCameraHandle, ENeptuneAcquisitionMode emAcqMode, UInt32 uiFrames);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcOneShot(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcMultiShot(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetBayerConvert(IntPtr hCameraHandle, ref ENeptuneBayerMethod pemMethod);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetBayerConvert(IntPtr hCameraHandle, ENeptuneBayerMethod emMethod);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetBayerLayout(IntPtr hCameraHandle, ref ENeptuneBayerLayout pemLayout);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetBayerLayout(IntPtr hCameraHandle, ENeptuneBayerLayout emLayout);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetRotation(IntPtr hCameraHandle, ref ENeptuneRotationAngle pemAngle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetRotation(IntPtr hCameraHandle, ENeptuneRotationAngle emAngle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetEffect(IntPtr hCameraHandle, ref Int32 pnEffectFlag);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetEffect(IntPtr hCameraHandle, Int32 nEffectFlag);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetCameraListOpt(ref ENeptuneCameraListOpt pemCameraListOpt);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetCameraListOpt(ENeptuneCameraListOpt emCameraListOpt);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetDisplayOption(ref ENeptuneDisplayOption pemDisplayOpt);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetDisplayOption(ENeptuneDisplayOption emDisplayOpt);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetDisplay(IntPtr hCameraHandle, IntPtr hWnd);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcShowControlDialog(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGrab(IntPtr hCameraHandle, ref NEPTUNE_IMAGE pImageInfo, ENeptuneGrabFormat emGrabFmt, UInt32 uiTimeOut);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetRGBData(IntPtr hCameraHandle, [Out] Byte[] pBuffer, UInt32 uiBufSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetRGB32Data(IntPtr hCameraHandle, [Out] Byte[] pBuffer, UInt32 uiBufSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSaveImage(IntPtr hCameraHandle, String pszFilePathName, UInt32 uiQuality);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcStartStreamCapture(IntPtr hCameraHandle, String pszFilePathName, ENeptuneBoolean emCompress, UInt32 uiBitrate, float fPlaySpeed);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcStopStreamCapture(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetFeature(IntPtr hCameraHandle, ENeptuneFeature emFeatureType, ref NEPTUNE_FEATURE pFeatureInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetFeature(IntPtr hCameraHandle, ENeptuneFeature emFeatureType, NEPTUNE_FEATURE stFeatureInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetPackageFeature(IntPtr hCameraHandle, ref NEPTUNE_PACKAGE_FEATURE pPackageFeature);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetPackageFeature(IntPtr hCameraHandle, NEPTUNE_PACKAGE_FEATURE stPackageFeature);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetExposureTime(IntPtr hCameraHandle, ref UInt32 puiMicroSec, ref UInt32 puiMin, ref UInt32 puiMax);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetExposureTime(IntPtr hCameraHandle, UInt32 uiMicroSec);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetShutterString(IntPtr hCameraHandle, String pszExposureTime);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetTriggerMode14Exposure(IntPtr hCameraHandle, UInt32 uiExposure, UInt32 uiInterval);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetTriggerInfo(IntPtr hCameraHandle, ref NEPTUNE_TRIGGER_INFO pTriggerInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetTrigger(IntPtr hCameraHandle, ref NEPTUNE_TRIGGER pTrigger);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetTrigger(IntPtr hCameraHandle, NEPTUNE_TRIGGER stTrigger);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetTriggerDelay(IntPtr hCameraHandle, ref UInt32 puiValue, ref UInt32 puiMin, ref UInt32 puiMax);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetTriggerDelay(IntPtr hCameraHandle, UInt32 uiValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcRunSWTrigger(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcRunSWTriggerEx(IntPtr hCameraHandle, UInt32 uiTimeout);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcReadTriggerTable(IntPtr hCameraHandle, ref NEPTUNE_TRIGGER_TABLE pTriggerTable);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSaveTriggerTable(IntPtr hCameraHandle, NEPTUNE_TRIGGER_TABLE stTriggerTable);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcLoadTriggerTable(IntPtr hCameraHandle, UInt32 uiIndex);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStrobeInfo(IntPtr hCameraHandle, ref NEPTUNE_STROBE_INFO pStrobeInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStrobe(IntPtr hCameraHandle, ref NEPTUNE_STROBE pStrobe);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStrobe(IntPtr hCameraHandle, NEPTUNE_STROBE stStrobe);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetAutoAreaControl(IntPtr hCameraHandle, ENeptuneAutoAreaSelect emSelect, ref NEPTUNE_AUTOAREA pAutoArea);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAutoAreaControl(IntPtr hCameraHandle, ENeptuneAutoAreaSelect emSelect, NEPTUNE_AUTOAREA stAutoArea);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAFControl(IntPtr hCameraHandle, ENeptuneAFMode emControlMode);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAutoIrisMode(IntPtr hCameraHandle, ENeptuneAutoIrisMode emAutoIrisMode);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetAutoIrisAverageFrame(IntPtr hCameraHandle, ref UInt32 puiValue, ref UInt32 puiMin, ref UInt32 puiMax);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAutoIrisAverageFrame(IntPtr hCameraHandle, UInt32 uiValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetAutoIrisTargetValue(IntPtr hCameraHandle, ref UInt32 puiValue, ref UInt32 puiMin, ref UInt32 puiMax);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetAutoIrisTargetValue(IntPtr hCameraHandle, UInt32 uiValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetBitsPerPixel(IntPtr hCameraHandle, ref UInt32 puiValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetBytePerPacket(IntPtr hCameraHandle, ref UInt32 puiValue, ref UInt32 puiMin, ref UInt32 puiMax);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetBytePerPacket(IntPtr hCameraHandle, UInt32 uiValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetPacketSize(IntPtr hCameraHandle, ref UInt32 puiValue, ref UInt32 puiMin, ref UInt32 puiMax);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetPacketSize(IntPtr hCameraHandle, UInt32 uiValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetPacketResend(IntPtr hCameraHandle, ENeptuneBoolean emEnable);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetBufferCount(IntPtr hCameraHandle, ref UInt32 puiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetBufferCount(IntPtr hCameraHandle, UInt32 uiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetUSBTriggerBufferCount(IntPtr hCameraHandle, UInt32 uiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetBufferSize(IntPtr hCameraHandle, ref UInt32 puiSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetRecvDroppedFrame(IntPtr hCameraHandle, ENeptuneBoolean emEnable);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetHeartbeatTime(IntPtr hCameraHandle, UInt32 ulMilliSecTime);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetMulticastAddress(IntPtr hCameraHandle, String pszAddress);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetUserSet(IntPtr hCameraHandle, ref NEPTUNE_USERSET pUserSet);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetUserSet(IntPtr hCameraHandle, NEPTUNE_USERSET stUserSet);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetDefaultUserSet(IntPtr hCameraHandle, ENeptuneUserSet emUserSet);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetPowerOnDefaultUserSet(IntPtr hCameraHandle, ENeptuneUserSet emUserSet);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSaveCameraParameter(IntPtr hCameraHandle, String pszFilePathName);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcLoadCameraParameter(IntPtr hCameraHandle, String pszFilePathName);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetKneeLUT(IntPtr hCameraHandle, ref NEPTUNE_KNEE_LUT pKneeLUT);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetKneeLUT(IntPtr hCameraHandle, NEPTUNE_KNEE_LUT stKneeLUT);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetUserLUT(IntPtr hCameraHandle, ref NEPTUNE_USER_LUT pUserLUT);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetUserLUT(IntPtr hCameraHandle, NEPTUNE_USER_LUT stUserLUT);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetFrameSave(IntPtr hCameraHandle, ref ENeptuneBoolean pemOnOff, ref UInt32 puiFrameRemained);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetFrameSave(IntPtr hCameraHandle, ENeptuneBoolean emOnOff, ENeptuneBoolean emTransfer, UInt32 uiFrames);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetGPIO(IntPtr hCameraHandle, NEPTUNE_GPIO stGpio);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcReadSIO(IntPtr hCameraHandle, ref NEPTUNE_SIO pData);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcWriteSIO(IntPtr hCameraHandle, NEPTUNE_SIO stData);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetSIO(IntPtr hCameraHandle, NEPTUNE_SIO_PROPERTY stProperty);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcReadRegister(IntPtr hCameraHandle, UInt32 ulAddress, ref UInt32 pulValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcWriteRegister(IntPtr hCameraHandle, UInt32 ulAddress, UInt32 ulValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcReadBlock(IntPtr hCameraHandle, UInt32 ulAddress, ref Byte pBuffer, ref UInt32 pulBufSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcWriteBlock(IntPtr hCameraHandle, UInt32 ulAddress, ref Byte pBuffer, UInt32 ulBufSize);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcWriteBroadcast(IntPtr hCameraHandle, UInt32 ulAddress, UInt32 ulValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeVisibility(IntPtr hCameraHandle, ref ENeptuneNodeVisibility pemVisibility);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeVisibility(IntPtr hCameraHandle, ENeptuneNodeVisibility emVisibility);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeList(IntPtr hCameraHandle, String pszParentNodeName, ref NEPTUNE_XML_NODE_LIST pNodeInfoList);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeListChar(IntPtr hCameraHandle, String pszParentNodeName, [Out] char[] pBuffer, UInt32 uiStrLength, ref UInt32 puiCount);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeInfo(IntPtr hCameraHandle, String pszNodeName, ref NEPTUNE_XML_NODE_INFO pNodeInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeInt(IntPtr hCameraHandle, String pszNodeName, ref NEPTUNE_XML_INT_VALUE_INFO pValueInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeInt(IntPtr hCameraHandle, String pszNodeName, Int64 nValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeFloat(IntPtr hCameraHandle, String pszNodeName, ref NEPTUNE_XML_FLOAT_VALUE_INFO pValueInfo);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeFloat(IntPtr hCameraHandle, String pszNodeName, Double dbValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeEnum(IntPtr hCameraHandle, String pszNodeName, ref NEPTUNE_XML_ENUM_LIST pEnumList);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeEnumChar(IntPtr hCameraHandle, String pszNodeName, [Out] char[] pBuffer, UInt32 uiStrLength, ref UInt32 puiCount, ref UInt32 puiIndex);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeEnum(IntPtr hCameraHandle, String pszNodeName, String pszValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeString(IntPtr hCameraHandle, String pszNodeName, [Out] char[] pBuffer, ref UInt32 puiBufSize, ref ENeptuneNodeAccessMode pemAccessMode);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeString(IntPtr hCameraHandle, String pszNodeName, String pszValue);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetNodeBoolean(IntPtr hCameraHandle, String pszNodeName, ref ENeptuneBoolean pemState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeBoolean(IntPtr hCameraHandle, String pszNodeName, ENeptuneBoolean emState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetNodeCommand(IntPtr hCameraHandle, String pszNodeName);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetDeviceCheckCallback(NeptuneCDevCheckCallback fpCallback, IntPtr pContext);
        
        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetUnplugCallback(IntPtr hCameraHandle, NeptuneCUnplugCallback fpCallback, IntPtr pContext);
        
        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetFrameCallback(IntPtr hCameraHandle, NeptuneCFrameCallback fpCallback, IntPtr pContext);
        
        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetFrameDropCallback(IntPtr hCameraHandle, NeptuneCFrameDropCallback fpCallback, IntPtr pContext);
        
        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetRecvTimeoutCallback(IntPtr hCameraHandle, NeptuneCRecvTimeoutCallback fpCallback, IntPtr pContext);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcInitCam4AltLed(IntPtr hCameraHandle);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcUpdateCam4AltLedTable(IntPtr hCameraHandle, Int32[] piData, Int32 iSize/* 255*64*sizeof(_int32_t) */);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetCam4AltLedIndex(IntPtr hCameraHandle, ENeptuneBoolean bAutoRun, Int32 iStart, Int32 iEnd);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetCam4AltLedDirect(IntPtr hCameraHandle, Int32 iIndex);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiControl(IntPtr hCameraHandle, ref ENeptuneBoolean pemState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiControl(IntPtr hCameraHandle, ENeptuneBoolean emState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiSelector(IntPtr hCameraHandle, ref UInt32 puiStackedRoiIdx);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiSelector(IntPtr hCameraHandle, UInt32 uiStackedRoiIdx);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiSelectedEnable(IntPtr hCameraHandle, ref ENeptuneBoolean pemState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiSelectedEnable(IntPtr hCameraHandle, ENeptuneBoolean emState);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiOffsetX(IntPtr hCameraHandle, ref UInt32 puiOffsetX);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiOffsetX(IntPtr hCameraHandle, UInt32 uiOffsetX);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiOffsetXAll(IntPtr hCameraHandle, UInt32 uiOffsetX);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiWidth(IntPtr hCameraHandle, ref UInt32 puiWidth);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiWidth(IntPtr hCameraHandle, UInt32 uiWidth);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiWidthAll(IntPtr hCameraHandle, UInt32 uiWidth);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiOffsetY(IntPtr hCameraHandle, ref UInt32 puiOffsetY);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiOffsetY(IntPtr hCameraHandle, UInt32 uiOffsetY);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcGetStackedRoiHeight(IntPtr hCameraHandle, ref UInt32 puiHeight);

        [DllImport(strFileName, CallingConvention = CallingConvention.StdCall)]
        public static extern ENeptuneError ntcSetStackedRoiHeight(IntPtr hCameraHandle, UInt32 uiHeight);
    }
}
