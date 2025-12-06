"use client";

import { render, screen } from "@testing-library/react";
import DashboardPage from "@/app/(app)/dashboard/page";
import { vi } from "vitest";

vi.mock("@/features/auth/components/logout-button", () => ({
  __esModule: true,
  default: () => <div data-testid="logout-button" />,
}));

const selectorMock = vi.fn();

vi.mock("@/store/hooks", () => ({
  useAppSelector: (fn: any) => selectorMock(fn),
}));

describe("DashboardPage gating", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("disables upload CTA when verification is needed", () => {
    selectorMock.mockReturnValue({ needsVerification: true });

    render(<DashboardPage />);

    expect(screen.getByRole("button", { name: /go to upload/i })).toBeDisabled();
    expect(
      screen.getByText(/verify your email to enable uploads/i)
    ).toBeInTheDocument();
  });

  it("enables upload CTA when verified", () => {
    selectorMock.mockReturnValue({ needsVerification: false });

    render(<DashboardPage />);

    expect(screen.getByRole("button", { name: /go to upload/i })).toBeEnabled();
  });
});
