import { useState } from "react";

export default function planDetail() {
  const [plan, setPlan] = useState("");

  return (
    <form>
      <label htmlFor="plan">Plan:</label>
      <input
        name="plan"
        id="plan"
        type="text"
        value={plan}
        onChange={(e) => {
          setPlan(e.target.value);
        }}
      />
      <button>Save</button>
      <button>Delete</button>
    </form>
  );
}
