import Confirmation from "../components/Confirmation";

export default function DeletePage({ resource, type }) {
  const onConfirm = () => {
    console.log("Delete");
  };

  const onCancel = () => {
    console.log("Go Back");
  };

  return (
    <Confirmation
      message={`Are you sure you want to delete this ${type}?`}
      onConfirm={onConfirm}
      onCancel={onCancel}
    />
  );
}
