import React from "react";
import PropTypes from "prop-types";
import { Navigate } from "react-router-dom";

const CarriersList = (props) => {
  if (!props.isAuthenticated()) {
    return <Navigate to="/login" replace />;
  } else {
    return (
      <div>
        <table className="table is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              {props.isAuthenticated() && <th />}
            </tr>
          </thead>
          <tbody>
            {props.carriers.map((carrier) => {
              return (
                <tr key={carrier.id}>
                  <td>{carrier.id}</td>
                  <td>{carrier.name}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
};

CarriersList.propTypes = {
  isAuthenticated: PropTypes.func.isRequired,
};

export default CarriersList;
