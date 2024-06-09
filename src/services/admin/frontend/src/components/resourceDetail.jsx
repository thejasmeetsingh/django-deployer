import instanceDetail from "./instanceDetail";
import planDetail from "./planDetail";

export default function ResourceDetail(type) {
  if (type === "plan") {
    return <planDetail />;
  }
  return <instanceDetail />;
}
