export default function Confirmation(message) {
  return (
    <div>
      <p>Are you sure you want to {message}</p>
      <button>Yes</button>
      <button>No</button>
    </div>
  );
}
