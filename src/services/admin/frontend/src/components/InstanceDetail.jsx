import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useInstanceContext from "../hooks/use-instance-context";

export default function InstanceDetail() {
  const [instanceName, setInstanceName] = useState("");
  const { id } = useParams();
  const { getInstanceByID } = useInstanceContext();

  useEffect(() => {
    async function fetchData() {
      const instance = await getInstanceByID(id);
      if (instance) {
        setInstanceName(instance.name);
      }
    }
    fetchData();
  }, []);

  return (
    <form>
      <label htmlFor="instanceName">instance:</label>
      <input
        name="instanceName"
        id="instanceName"
        type="text"
        value={instanceName}
        onChange={(e) => {
          setInstanceName(e.target.value);
        }}
      />
      <button>Save</button>
      <button>Delete</button>
    </form>
  );
}
