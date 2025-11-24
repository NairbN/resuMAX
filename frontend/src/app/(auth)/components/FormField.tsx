import type { InputHTMLAttributes } from "react";
import { Input } from "./Input";

type FormFieldProps = {
  label: string;
} & InputHTMLAttributes<HTMLInputElement> &
  Required<Pick<InputHTMLAttributes<HTMLInputElement>, "id">>;

export function FormField({ label, id, ...inputProps }: FormFieldProps) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-white/90" htmlFor={id}>
        {label}
      </label>
      <Input id={id} {...inputProps} />
    </div>
  );
}
