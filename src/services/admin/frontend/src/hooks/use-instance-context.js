import { useContext } from "react";
import { InstanceContext } from "../context/instance";

export default function useInstanceContext() {
  return useContext(InstanceContext);
}
