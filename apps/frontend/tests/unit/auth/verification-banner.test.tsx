import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import VerificationBanner from "@/features/auth/components/verification-banner";
import { vi } from "vitest";

const dispatchMock = vi.fn();
const selectorMock = vi.fn();

vi.mock("@/store/hooks", () => ({
  useAppDispatch: () => dispatchMock,
  useAppSelector: (fn: any) => selectorMock(fn),
}));

describe("VerificationBanner", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("does not render when verification is not needed", () => {
    selectorMock.mockReturnValue({
      needsVerification: false,
      status: "authenticated",
      error: null,
    });

    const { container } = render(<VerificationBanner />);
    expect(container).toBeEmptyDOMElement();
  });

  it("renders and triggers resend", async () => {
    selectorMock.mockReturnValue({
      needsVerification: true,
      status: "idle",
      error: null,
    });
    dispatchMock.mockReturnValue(Promise.resolve());

    render(<VerificationBanner />);

    expect(
      screen.getByText(/email not verified/i)
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: /resend/i }));
    expect(dispatchMock).toHaveBeenCalled();
  });
});
