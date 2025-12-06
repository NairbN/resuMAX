import { api } from "@/services/api/client";

describe("CSRF interceptor", () => {
  it("sets X-CSRF-Token header on mutating requests when cookie present", () => {
    Object.defineProperty(document, "cookie", {
      writable: true,
      value: "XSRF-TOKEN=test-token",
    });

    const config = api.interceptors.request.handlers[0].fulfilled?.({
      method: "post",
      headers: {},
    } as any);

    expect((config?.headers as any)["X-CSRF-Token"]).toBe("test-token");
  });

  it("does not set header on GET requests", () => {
    Object.defineProperty(document, "cookie", {
      writable: true,
      value: "XSRF-TOKEN=test-token",
    });

    const config = api.interceptors.request.handlers[0].fulfilled?.({
      method: "get",
      headers: {},
    } as any);

    expect((config?.headers as any)["X-CSRF-Token"]).toBeUndefined();
  });
});
