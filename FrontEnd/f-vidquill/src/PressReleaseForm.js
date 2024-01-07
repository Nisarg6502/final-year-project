// PressReleaseForm.js

import React, { useState } from 'react';
import './PressReleaseForm.css';

const PressReleaseForm = ({ onSubmit }) => {
 const [pressRelease, setPressRelease] = useState('');
 const [submittedText, setSubmittedText] = useState('');

 const handleInputChange = (e) => {
    setPressRelease(e.target.value);
 };

 const handleSubmit = (e) => {
    e.preventDefault();
    // Call the onSubmit prop and pass the press release data
    onSubmit(pressRelease);
    // Update submittedText to display the input text below
    setSubmittedText(pressRelease);
    // Clear the pressRelease input after submission
    setPressRelease('');
 };

 return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <label>
          Press Release:
          <br/>
          <textarea
            value={pressRelease}
            onChange={handleInputChange}
            rows={4}
            cols={50}
            className="text-area"
          />
        </label>
        <br />
        <br />
        <button type="submit" className="submit-button">Generate Text</button>
      </form>
      {submittedText && (
        <div className="submitted-text">
          <p>Submitted Text:</p>
          <p>{submittedText}</p>
        </div>
      )}
    </div>
 );
};

export default PressReleaseForm;
