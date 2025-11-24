import { useEffect, useState } from "react";
import { getMockDashboardData, type DashboardData } from "@/app/(dashboard)/lib/dashboard-data";

export function useDashboardData() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    // Replace with real API call when backend is ready.
    setData(getMockDashboardData());
  }, []);

  return data;
}
