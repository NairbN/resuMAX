import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Login from "@/features/auth/components/login";
import { vi } from "vitest";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}));

const dispatchMock = vi.fn();
const selectorMock = vi.fn();
const loginThunk = vi.fn().mockReturnValue("login-thunk");

vi.mock("@/store/hooks", () => ({
  useAppDispatch: () => dispatchMock,
  useAppSelector: (fn: any) => selectorMock(fn),
}));

vi.mock("@/features/auth/store/thunks", () => ({
  login: (...args: any[]) => loginThunk(...args),
}));

describe("Login component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    selectorMock.mockReturnValue({
      status: "idle",
      error: null,
      errorStatus: null,
      needsVerification: false,
    });
    dispatchMock.mockReturnValue({
      unwrap: () => Promise.resolve({ needsVerification: false }),
    });
  });

  it("submits valid credentials and dispatches login", async () => {
    render(<Login />);

    await userEvent.type(screen.getByLabelText(/email/i), "user@example.com");
    await userEvent.type(screen.getByLabelText(/password/i), "password123");
    await userEvent.click(screen.getByRole("button", { name: /continue with email/i }));

    expect(loginThunk).toHaveBeenCalledWith({
      email: "user@example.com",
      password: "password123",
    });
    expect(dispatchMock).toHaveBeenCalledWith("login-thunk");
  });

  it("shows 401 error message", () => {
    selectorMock.mockReturnValue({
      status: "idle",
      error: "Bad credentials",
      errorStatus: 401,
      needsVerification: false,
    });

    render(<Login />);

    expect(screen.getByText(/invalid email or password/i)).toBeInTheDocument();
  });

  it("shows 429 error message", () => {
    selectorMock.mockReturnValue({
      status: "idle",
      error: "Rate limited",
      errorStatus: 429,
      needsVerification: false,
    });

    render(<Login />);

    expect(screen.getByText(/too many attempts/i)).toBeInTheDocument();
  });
});
