import React, { useState } from 'react';
import { motion } from 'motion/react';

interface SparkleStarProps {
  size?: number;
  className?: string;
  fill?: string;
  animate?: boolean;
  interactive?: boolean;
  onClick?: () => void;
}

export const SparkleStar: React.FC<SparkleStarProps> = ({
  size = 48,
  className = '',
  fill = 'currentColor',
  animate = false,
  interactive = true,
  onClick,
}) => {
  const [clickSpins, setClickSpins] = useState(0);

  const handleClick = () => {
    if (interactive) {
      setClickSpins((prev) => prev + 1);
    }
    if (onClick) {
      onClick();
    }
  };

  return (
    <motion.svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      onClick={handleClick}
      whileHover={interactive ? { scale: 1.22, rotate: 90, transition: { type: 'spring', stiffness: 350, damping: 14 } } : undefined}
      whileTap={interactive ? { scale: 0.82, rotate: -45 } : undefined}
      animate={{
        rotate: clickSpins * 180,
      }}
      transition={{ type: 'spring', stiffness: 260, damping: 16 }}
      className={`inline-block select-none ${interactive ? 'cursor-pointer' : ''} ${className}`}
    >
      <path
        d="M50 0 C50 32 32 50 0 50 C32 50 50 68 50 100 C50 68 68 50 100 50 C68 50 50 32 50 0 Z"
        fill={fill}
      />
    </motion.svg>
  );
};
