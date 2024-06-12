import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <form
      method="post"
      onSubmit={(e) => {
        e.preventDefault();
        console.log(email, password);
        setEmail("");
        setPassword("");
      }}
    >
      <label htmlFor="email">Email:</label>
      <input
        id="email"
        name="email"
        type="text"
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);
        }}
      />
      <label htmlFor="password">Password:</label>
      <input
        id="password"
        name="password"
        type="password"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value);
        }}
      />
      <button type="submit">Login</button>
    </form>
  );
}
