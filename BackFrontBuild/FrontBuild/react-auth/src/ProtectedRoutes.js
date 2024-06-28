import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Cookies from "universal-cookie";
const cookies = new Cookies();

// receives component and any other props represented by ...rest
export default function ProtectedRoutes({ element: Element, ...rest }) {
  return (
    <Router>

      <Routes>
          // this route takes other route assigned to it from the App.js and return the same route if condition is met
          <Route
            {...rest}
            render={(props) => {
              // get cookie from browser if logged in
              const token = cookies.get("TOKEN");

              // return route if there is a valid token set in the cookie
              if (token) {
                return <Element {...props} />;
              } else {
                // return the user to the landing page if there is no valid token set
                return (
                  <Navigate 
                    to={{
                      pathname: "/",
                      state: {
                        // sets the location a user was about to assess before being redirected to login
                        from: props.location,
                      },
                    }}
                  />
                );
              }
            }}
          />
      </Routes>

    </Router>
  );
}

// function App() {
//   return (
//     <Routes>
//       <Route path="/public" element={<PublicPage />} />
//       <Route
//         path="/protected"
//         element={
//           // Good! Do your composition here instead of wrapping <Route>.
//           // This is really just inverting the wrapping, but it's a lot
//           // more clear which components expect which props.
//           <RequireAuth redirectTo="/login">
//             <ProtectedPage />
//           </RequireAuth>
//         }
//       />
//     </Routes>
//   );
// }

// function RequireAuth({ children, redirectTo }) {
//   let isAuthenticated = getAuth();
//   return isAuthenticated ? children : <Navigate to={redirectTo} />;
// }