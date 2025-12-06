"use client";

import { Button } from "@/components/ui/button";

type Props = {
  onLogin: () => void;
  onSignup: () => void;
  style?: React.CSSProperties;
};

const AuthCtaButtons = ({ onLogin, onSignup, style }: Props) => {
  return (
    <div className="mt-10 flex items-center justify-center gap-4" style={style}>
      <Button
        size="lg"
        variant="outline"
        onClick={onLogin}
        className="bg-transparent border border-slate-300 text-slate-900 hover:bg-slate-100 hover:text-slate-900 dark:border-white/60 dark:text-white dark:hover:bg-white/10 dark:hover:text-white"
      >
        Log in
      </Button>
      <Button
        size="lg"
        variant="default"
        className="bg-primary text-primary-foreground hover:bg-primary/90"
        onClick={onSignup}
      >
        Sign Up
      </Button>
    </div>
  );
};

export default AuthCtaButtons;
