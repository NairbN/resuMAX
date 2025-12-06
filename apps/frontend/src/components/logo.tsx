import Image from "next/image";
import { cn } from "@/lib/utils";

type LogoProps = {
  className?: string;
  size?: number;
};

export const Logo = ({ className, size = 28 }: LogoProps) => {
  return (
    <Image
      src="/logo.svg"
      alt="ResuMAX logo"
      width={size}
      height={size}
      className={cn(className)}
      style={{ width: `${size}px`, height: "auto", objectFit: "contain" }}
      priority
    />
  );
};
