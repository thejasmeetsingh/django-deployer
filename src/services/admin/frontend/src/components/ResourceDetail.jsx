import instanceDetail from "./InstanceDetail";
import planDetail from "./PlanDetail";

export default function ResourceDetail({ resource, type }) {
  if (type === "plan") {
    return <planDetail />;
  }
  return <instanceDetail />;
}
