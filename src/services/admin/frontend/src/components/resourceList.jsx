import { useState } from "react";

export default function ResourceList() {
  const [resources, addResource] = useState([]);

  const renderResource = resources.map((resource, idx) => {
    return <div id={idx}>{resource.name}</div>;
  });

  return <div>{renderResource}</div>;
}
