import { useState } from "react";

export default function instanceDetail() {
  const [instance, setInstance] = useState("");

  return (
    <form>
      <label htmlFor="instance">instance:</label>
      <input
        name="instance"
        id="instance"
        type="text"
        value={instance}
        onChange={(e) => {
          setInstance(e.target.value);
        }}
      />
      <button>Save</button>
      <button>Delete</button>
    </form>
  );
}
