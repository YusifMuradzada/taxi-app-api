import { useEffect, useState } from "react";

import LoginModal from "../components/LoginModal";
import Map from "../components/Map";

function calculateDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
) {
  const R = 6371;

  const dLat =
    ((lat2 - lat1) * Math.PI) / 180;

  const dLon =
    ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(dLat / 2) *
      Math.sin(dLat / 2) +
    Math.cos(
      (lat1 * Math.PI) / 180
    ) *
      Math.cos(
        (lat2 * Math.PI) / 180
      ) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);

  const c =
    2 *
    Math.atan2(
      Math.sqrt(a),
      Math.sqrt(1 - a)
    );

  return R * c;
}

function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [loginOpen, setLoginOpen] = useState(false);

  const [user, setUser] = useState<any>(null);

  const [pickupLocation, setPickupLocation] =
    useState("");

  const [destination, setDestination] =
    useState("");

  const [pickup, setPickup] = useState<{
    latitude: number;
    longitude: number;
  } | null>(null);

  const [destinationPoint, setDestinationPoint] =
    useState<{
      latitude: number;
      longitude: number;
    } | null>(null);

  const [rideType, setRideType] =
    useState("Eco");

  const [loading, setLoading] =
    useState(false);

  const [ride, setRide] =
    useState<any>(null);

  const handleLogout = () => {
    localStorage.removeItem("token");

    setUser(null);
    setMenuOpen(false);
  };

  useEffect(() => {
    const token =
      localStorage.getItem("token");

    if (!token) {
      return;
    }

    fetch(
      "http://127.0.0.1:8000/users/me",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            "Unauthorized"
          );
        }

        return response.json();
      })
      .then((data) => {
        setUser(data);
      })
      .catch(() => {
        localStorage.removeItem(
          "token"
        );

        setUser(null);
      });
  }, []);

  const handleFindRide = async () => {
    const token =
      localStorage.getItem("token");

    if (!token) {
      setLoginOpen(true);
      return;
    }

    if (!pickup || !destinationPoint) {
      alert(
        "Please select pickup and destination on the map."
      );

      return;
    }

    if (
      !pickupLocation ||
      !destination
    ) {
      alert(
        "Please enter pickup location and destination."
      );

      return;
    }

    const distance =
      calculateDistance(
        pickup.latitude,
        pickup.longitude,
        destinationPoint.latitude,
        destinationPoint.longitude
      );

    setLoading(true);

    try {
      const response =
        await fetch(
          "http://127.0.0.1:8000/rides/",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",

              Authorization: `Bearer ${token}`,
            },

            body: JSON.stringify({
              pickup_location:
                pickupLocation,

              destination:
                destination,

              pickup_latitude:
                pickup.latitude,

              pickup_longitude:
                pickup.longitude,

              distance_km: Number(
                distance.toFixed(2)
              ),
            }),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {
        alert(
          JSON.stringify(
            data.detail,
            null,
            2
          )
        );

        return;
      }

      setRide(data);
    } catch (error) {
      alert(
        "Serverə qoşulmaq mümkün olmadı"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <header className="navbar">
        <button
          className="logo"
          onClick={() =>
            (window.location.href = "/")
          }
        >
          🚕 TAXIGO
        </button>

        <nav>
          <a href="#">
            Home
          </a>

          <a href="#">
            About
          </a>

          {!user ? (
            <button
              className="login-link"
              onClick={() =>
                setLoginOpen(true)
              }
            >
              Login
            </button>
          ) : (
            <span className="user-name">
              👤 {user.name}
            </span>
          )}

          <button
            className="menu-button"
            onClick={() =>
              setMenuOpen(!menuOpen)
            }
          >
            ☰
          </button>
        </nav>

        {menuOpen && (
          <div className="menu">
            <a href="#">
              Help
            </a>

            <a href="#">
              Ride history
            </a>

            <a href="#">
              Settings
            </a>

            <a href="#">
              Contact
            </a>

            {user && (
              <button
                className="logout-button"
                onClick={
                  handleLogout
                }
              >
                Logout
              </button>
            )}
          </div>
        )}
      </header>

      <main className="main-content">
        <section className="map">
          <Map
            pickup={pickup}
            destination={
              destinationPoint
            }
            onPickupSelect={(
              latitude,
              longitude
            ) => {
              setPickup({
                latitude,
                longitude,
              });

              setPickupLocation(
                `${latitude.toFixed(
                  5
                )}, ${longitude.toFixed(
                  5
                )}`
              );
            }}
            onDestinationSelect={(
              latitude,
              longitude
            ) => {
              setDestinationPoint({
                latitude,
                longitude,
              });

              setDestination(
                `${latitude.toFixed(
                  5
                )}, ${longitude.toFixed(
                  5
                )}`
              );
            }}
          />
        </section>

        <section className="booking-card">
          <input
            type="text"
            placeholder="📍 Start location"
            value={
              pickupLocation
            }
            onChange={(e) =>
              setPickupLocation(
                e.target.value
              )
            }
          />

          <input
            type="text"
            placeholder="🏁 Destination"
            value={destination}
            onChange={(e) =>
              setDestination(
                e.target.value
              )
            }
          />

          <div className="ride-types">
            <button
              className={
                rideType === "Eco"
                  ? "selected-ride"
                  : ""
              }
              onClick={() =>
                setRideType(
                  "Eco"
                )
              }
            >
              🚕 Eco
            </button>

            <button
              className={
                rideType ===
                "Priority"
                  ? "selected-ride"
                  : ""
              }
              onClick={() =>
                setRideType(
                  "Priority"
                )
              }
            >
              ⚡ Priority
            </button>

            <button
              className={
                rideType ===
                "Premium"
                  ? "selected-ride"
                  : ""
              }
              onClick={() =>
                setRideType(
                  "Premium"
                )
              }
            >
              🚘 Premium
            </button>
          </div>

          <button
            className="find-ride"
            onClick={
              handleFindRide
            }
            disabled={loading}
          >
            {loading
              ? "Finding a ride..."
              : "Find a ride"}
          </button>

          <button className="cargo-button">
            📦 Send a package
          </button>
        </section>

        {ride && (
          <section className="ride-status-card">
            <div className="ride-status-header">
              <div>
                <h2>
                  🚕 Ride requested
                </h2>

                <p>
                  We are looking for
                  a driver
                </p>
              </div>

              <span className="ride-status">
                {ride.status}
              </span>
            </div>

            <div className="route">
              <div className="route-item">
                <span className="route-icon">
                  📍
                </span>

                <div>
                  <small>
                    Pickup
                  </small>

                  <strong>
                    {
                      ride.pickup_location
                    }
                  </strong>
                </div>
              </div>

              <div className="route-line"></div>

              <div className="route-item">
                <span className="route-icon">
                  🏁
                </span>

                <div>
                  <small>
                    Destination
                  </small>

                  <strong>
                    {
                      ride.destination
                    }
                  </strong>
                </div>
              </div>
            </div>

            <div className="ride-info">
              <div>
                <small>
                  Distance
                </small>

                <strong>
                  {
                    ride.distance_km
                  }{" "}
                  km
                </strong>
              </div>

              <div>
                <small>
                  Ride ID
                </small>

                <strong>
                  #{ride.id}
                </strong>
              </div>
            </div>

            {ride.status ===
              "accepted" ? (
              <div className="driver-found">
                🚕 Driver found!

                <span>
                  Your driver has
                  accepted the
                  ride.
                </span>
              </div>
            ) : ride.status ===
              "started" ? (
              <div className="ride-started">
                🚕 Ride in progress

                <span>
                  Your ride has
                  started.
                </span>
              </div>
            ) : ride.status ===
              "completed" ? (
              <div className="ride-completed">
                ✅ Ride completed

                <span>
                  Price: $
                  {ride.price}
                </span>
              </div>
            ) : (
              <div className="searching-driver">
                🔎 Searching for a
                driver...
              </div>
            )}
          </section>
        )}
      </main>

      {loginOpen && (
        <LoginModal
          onClose={() =>
            setLoginOpen(false)
          }
        />
      )}
    </div>
  );
}

export default Home;