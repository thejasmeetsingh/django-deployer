import Confirmation from "../components/Confirmation";

export default function LogoutPage() {
  const onConfirm = () => {
    console.log("Logout");
  };

  const onCancel = () => {
    console.log("Go Back");
  };

  return (
    <Confirmation
      message="Are you sure you want to logout?"
      onConfirm={onConfirm}
      onCancel={onCancel}
    />
  );
}
