import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SignUp from "@/features/auth/components/signup";
import { vi } from "vitest";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}));

const dispatchMock = vi.fn();
const selectorMock = vi.fn();
const signupThunk = vi.fn().mockReturnValue("signup-thunk");

vi.mock("@/store/hooks", () => ({
  useAppDispatch: () => dispatchMock,
  useAppSelector: (fn: any) => selectorMock(fn),
}));

vi.mock("@/features/auth/store/thunks", () => ({
  signup: (...args: any[]) => signupThunk(...args),
}));

describe("SignUp component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    selectorMock.mockReturnValue({
      status: "idle",
      error: null,
      errorStatus: null,
      needsVerification: false,
    });
    dispatchMock.mockReturnValue({
      unwrap: () => Promise.resolve({ needsVerification: true }),
    });
  });

  it("requires matching passwords", async () => {
    render(<SignUp />);

    await userEvent.type(screen.getByLabelText(/^email/i), "user@example.com");
    await userEvent.type(screen.getByLabelText(/^password$/i), "password123");
    await userEvent.type(
      screen.getByLabelText(/confirm password/i),
      "different"
    );

    await userEvent.click(screen.getByRole("button", { name: /continue with email/i }));

    expect(screen.getByText(/passwords must match/i)).toBeInTheDocument();
    expect(signupThunk).not.toHaveBeenCalled();
  });

  it("submits when passwords match", async () => {
    render(<SignUp />);

    await userEvent.type(screen.getByLabelText(/^email/i), "user@example.com");
    await userEvent.type(screen.getByLabelText(/^password$/i), "password123");
    await userEvent.type(
      screen.getByLabelText(/confirm password/i),
      "password123"
    );

    await userEvent.click(screen.getByRole("button", { name: /continue with email/i }));

    expect(signupThunk).toHaveBeenCalledWith({
      email: "user@example.com",
      password: "password123",
      confirmPassword: "password123",
    });
    expect(dispatchMock).toHaveBeenCalledWith("signup-thunk");
  });
});
