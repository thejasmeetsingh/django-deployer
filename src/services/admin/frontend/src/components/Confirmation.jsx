export default function Confirmation({ message, onConfirm, onCancel }) {
  return (
    <div>
      <p>{message}</p>
      <button onClick={onConfirm}>Yes</button>
      <button onClick={onCancel}>No</button>
    </div>
  );
}
