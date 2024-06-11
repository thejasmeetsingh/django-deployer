import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import HomePage from "./pages/HomePage";
import PlanPage from "./pages/PlanPage";
import PlanDetailPage from "./pages/PlanDetailPage";
import InstancePage from "./pages/InstancePage";
import InstanceDetailPage from "./pages/InstanceDetailPage";
import LogoutPage from "./pages/LogoutPage";
import DeletePage from "./pages/DeletePage";
import { InstanceProvider } from "./context/instance";
import { PlanProvider } from "./context/plan";

function App() {
  return (
    <InstanceProvider>
      <PlanProvider>
        <Router>
          <Routes>
            <Route path="/" Component={Login} />
            <Route path="/home" Component={HomePage} />
            <Route path="/Logout" Component={LogoutPage} />
            <Route path="/plan" Component={PlanPage} />
            <Route path="/plan/:id" Component={PlanDetailPage} />
            <Route path="/plan/:id/delete" Component={DeletePage} />
            <Route path="/instance" Component={InstancePage} />
            <Route path="/instance/:id" Component={InstanceDetailPage} />
            <Route path="/instance/:id/delete" Component={DeletePage} />
          </Routes>
        </Router>
      </PlanProvider>
    </InstanceProvider>
  );
}

export default App;
