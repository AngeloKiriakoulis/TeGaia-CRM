import { useState } from "react";
import "./ContactForm.css";

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: "",
    number: "",
    email: "",
    message: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(null);

    try {
      const response = await fetch(
        "https://script.google.com/macros/s/AKfycbwl6_3Qz4YZwf5QPCKLWwrH9AVd4dz4XDfUzlc_Yqs7ZGfkBH8iMf93iT40B-h5G2vstQ/exec",
        {
          method: "POST",
          body: new URLSearchParams(formData),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      if (response.ok) {
        setSuccess("Your message has been sent!");
        setFormData({ name: "", number: "", email: "", message: "" });
      } else {
        setSuccess("Something went wrong. Try again later.");
      }
    } catch (error) {
      setSuccess("Network error. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h4>Contact Us</h4>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input type="text" name="number" placeholder="Number" value={formData.number} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <textarea name="message" rows="4" placeholder="Your Message" value={formData.message} onChange={handleChange} required />
        <button type="submit" id="submit" disabled={loading}>
          {loading ? "Sending..." : "Submit"}
        </button>
      </form>
      {success && <p className="success-message">{success}</p>}
    </div>
  );
}