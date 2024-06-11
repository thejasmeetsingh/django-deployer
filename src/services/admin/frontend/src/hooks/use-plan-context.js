import { useContext } from "react";
import { PlanContext } from "../context/plan";

export default function usePlanContext() {
  return useContext(PlanContext);
}
