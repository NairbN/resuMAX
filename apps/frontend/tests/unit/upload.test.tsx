"use client";

import { render, screen } from "@testing-library/react";
import UploadPage from "@/app/(app)/upload/page";
import { vi } from "vitest";

const selectorMock = vi.fn();

vi.mock("@/store/hooks", () => ({
  useAppSelector: (fn: any) => selectorMock(fn),
}));

describe("UploadPage gating", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("disables upload button when verification is needed", () => {
    selectorMock.mockReturnValue({ needsVerification: true });

    render(<UploadPage />);

    expect(screen.getByRole("button", { name: /upload file/i })).toBeDisabled();
    expect(
      screen.getByText(/verify your email to enable uploads/i)
    ).toBeInTheDocument();
  });

  it("enables upload button when verified", () => {
    selectorMock.mockReturnValue({ needsVerification: false });

    render(<UploadPage />);

    expect(screen.getByRole("button", { name: /upload file/i })).toBeEnabled();
  });
});
