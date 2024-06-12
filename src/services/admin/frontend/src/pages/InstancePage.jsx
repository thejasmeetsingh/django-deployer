import { useEffect } from "react";
import ResourceList from "../components/ResourceList";
import useInstanceContext from "../hooks/use-instance-context";

export default function InstancePage() {
  const { instances, fetchInstances } = useInstanceContext();

  useEffect(() => {
    fetchInstances();
  }, []);

  return (
    <div>
      <ResourceList resources={instances} baseURL="instance" />
    </div>
  );
}
