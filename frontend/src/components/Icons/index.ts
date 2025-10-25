/**
 * Centralized Icon System
 * All react-icons are organized here by category for better maintainability
 */

// Material Design Icons
export {
  MdRestaurant,
  MdLocationOn,
  MdShare,
  MdRocket,
  MdCategory,
  MdPlace,
  MdStorage,
  MdSpeed,
  MdSchool,
  MdFavorite,
  MdAndroid,
  MdHome,
  MdSearch,
  MdFilterList,
  MdStar,
  MdStarBorder,
  MdPhone,
  MdEmail,
  MdDirections,
  MdMoreVert,
  MdClose,
  MdMenu,
  MdArrowBack,
  MdArrowForward,
  MdExpandMore,
  MdExpandLess,
  MdRefresh,
  MdSettings,
} from 'react-icons/md';

// Font Awesome Icons
export {
  FaBuilding,
  FaCopyright,
  FaUser,
  FaUserCircle,
  FaHeart,
  FaMapMarkerAlt,
  FaUtensils,
  FaClock,
  FaDollarSign,
  FaGithub,
  FaLinkedin,
  FaTwitter,
  FaFacebook,
  FaInstagram,
} from 'react-icons/fa';

// Heroicons
export {
  HiSparkles,
  HiLightBulb,
  HiChat,
  HiChatAlt2,
  HiThumbUp,
  HiThumbDown,
  HiEye,
  HiEyeOff,
  HiExternalLink,
  HiDownload,
  HiUpload,
  HiInformationCircle,
  HiExclamationCircle,
  HiCheckCircle,
  HiXCircle,
} from 'react-icons/hi';

// Business and UI Icons
export {
  BiRestaurant,
  BiMap,
  BiTime,
  BiPhone,
  BiGlobe,
  BiChat,
  BiLike,
  BiDislike,
  BiBookmark,
  BiShare,
} from 'react-icons/bi';

// Additional useful icons
export {
  AiOutlineLoading3Quarters,
  AiFillStar,
  AiOutlineStar,
} from 'react-icons/ai';

export {
  IoMdArrowRoundBack,
  IoMdArrowRoundForward,
  IoMdCheckmark,
  IoMdClose,
} from 'react-icons/io';

// Icon type definitions for better TypeScript support
export type IconComponent = React.ComponentType<{
  className?: string;
  size?: string | number;
  color?: string;
}>;

// Common icon props for consistency
export const iconSizes = {
  xs: '12px',
  sm: '16px',
  md: '20px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
} as const;

export const iconColors = {
  primary: 'text-blue-600',
  secondary: 'text-gray-600', 
  success: 'text-green-600',
  warning: 'text-yellow-600',
  error: 'text-red-600',
  white: 'text-white',
  black: 'text-black',
} as const;

// Utility function to get consistent icon props
export function getIconProps(size: keyof typeof iconSizes = 'md', color?: keyof typeof iconColors) {
  return {
    size: iconSizes[size],
    className: color ? iconColors[color] : undefined,
  };
}