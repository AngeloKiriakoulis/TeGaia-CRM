import { useState } from "react";
import "./ContactForm.css";

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: "",
    number: "",
    email: "",
    company: "",
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
      const GOOGLE_SCRIPT_URL = import.meta.env.VITE_GOOGLE_SCRIPT_URL;

      if (!GOOGLE_SCRIPT_URL) {
        console.error("Google Script URL is missing!");
        return;
      }

      const response = await fetch(
        GOOGLE_SCRIPT_URL,
        {
          method: "POST",
          body: new URLSearchParams(formData),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      if (response.ok) {
        setSuccess("Your contact has been saved!");
        setFormData({ name: "", number: "", email: "", company: "", message: "" });
      } else {
        setSuccess("Something went wrong. Try again later.");
      }
    } catch (error) {
      setSuccess("Network error. Please try again.");
    }
    setLoading(false);
    
    try {
      const response = await fetch("https://tegaia-crm.vercel.app/api/contact", { 
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      const result = await response.json();
      if (result && typeof result.success === 'string') {
        setSuccess(result.success);
      } else {
        // Handle unexpected structure in result
        setSuccess(result.detail || "An unexpected error occurred.");
      }
    } catch (error) {
      setSuccess("E-mail couldn't be sent.");
    }
    // Reset success message after 3-4 seconds
    if (success) {
      setTimeout(() => {
        setSuccess(null);
      }, 4000); // 4000ms = 4 seconds
    }
  };

  return (
    <div className="container">
      <img src="/TeGaia-logo-11.svg" alt="Company Logo" className="company-logo" />
      <h4>Contact Us</h4>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input type="text" name="number" placeholder="Number" value={formData.number} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input type="text" name="company" placeholder="Company Name" value={formData.company} onChange={handleChange} required />
        <textarea name="message" rows="4" placeholder="Additional Notes" value={formData.message} onChange={handleChange} />
        <button type="submit" id="submit" disabled={loading}>
          {loading ? "Sending..." : "Submit"}
        </button>
      </form>
      {success && <p className="success-message">{success}</p>}
    </div>
  );
}
