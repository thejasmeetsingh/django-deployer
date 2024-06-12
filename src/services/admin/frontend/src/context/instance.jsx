import { createContext, useState } from "react";

const InstanceContext = createContext();

function InstanceProvider({ children }) {
  // ToDo: Replace static data manipulation with API calls
  const [instances, setInstance] = useState([]);

  const fetchInstances = async () => {
    setInstance([
      { id: 1, name: "t2.micro" },
      { id: 2, name: "t2.small" },
      { id: 3, name: "t2.medium" },
    ]);
  };

  const getInstanceByID = async (id) => {
    return { id: 1, name: "t2.micro" };
  };

  const createInstance = async (name) => {
    setInstance([...instances, { id: instances.length + 1, name }]);
  };

  const editInstance = async (id, name) => {
    setInstance(
      instances.map((instance, index) => {
        if (index === id) {
          return { ...instance, name };
        }
        return instance;
      })
    );
  };

  const deleteInstance = async (id) => {
    setInstance(
      instances.filter((_, index) => {
        return index !== id;
      })
    );
  };

  return (
    <InstanceContext.Provider
      value={{
        instances,
        fetchInstances,
        createInstance,
        getInstanceByID,
        editInstance,
        deleteInstance,
      }}
    >
      {children}
    </InstanceContext.Provider>
  );
}

export { InstanceContext, InstanceProvider };
