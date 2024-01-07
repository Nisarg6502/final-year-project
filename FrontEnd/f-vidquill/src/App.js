// App.js

import React from 'react';
import PressReleaseForm from './PressReleaseForm';
import IntroductionSection from './IntroductionSection';

const App = () => {
  const handlePressReleaseSubmit = (pressRelease) => {
    // Send pressRelease data to your backend for processing
    console.log('Press Release submitted:', pressRelease);
    // Add logic to send data to your backend
  };

  return (
    <div>
      <IntroductionSection />
      <PressReleaseForm onSubmit={handlePressReleaseSubmit} />
    </div>
  );
};

export default App;
