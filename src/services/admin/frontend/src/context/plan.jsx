import { createContext, useState } from "react";

const PlanContext = createContext();

function PlanProvider({ children }) {
  // ToDo: Replace static data manipulation with API calls
  const [plans, setPlan] = useState([]);

  const fetchPlans = async () => {
    setPlan([
      { id: 1, name: "plan 1" },
      { id: 2, name: "plan 2" },
      { id: 3, name: "plan 3" },
    ]);
  };

  const createPlan = async (name) => {
    setPlan([...plans, { id: plans.length + 1, name }]);
  };

  const getPlanByID = async (id) => {
    return { id: 1, name: "plan 1" };
  };

  const editPlan = async (id, name) => {
    setPlan(
      plans.map((plan, index) => {
        if (index === id) {
          return { ...plan, name };
        }
        return plan;
      })
    );
  };

  const deletePlan = async (id) => {
    setPlan(
      plans.filter((_, index) => {
        return index !== id;
      })
    );
  };

  return (
    <PlanContext.Provider
      value={{
        plans,
        fetchPlans,
        createPlan,
        getPlanByID,
        editPlan,
        deletePlan,
      }}
    >
      {children}
    </PlanContext.Provider>
  );
}

export { PlanContext, PlanProvider };
