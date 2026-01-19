export default {
  title: 'Components/Input',
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Form input components including text inputs, textareas, and validation states.',
      },
    },
  },
};

const inputBaseStyles = `
  display: block;
  width: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 16px;
  color: #171717;
  background-color: white;
  border: 1px solid #d4d4d4;
  border-radius: 6px;
  transition: border-color 0.15s ease-out, box-shadow 0.15s ease-out;
`;

export const TextInput = {
  render: () => `
    <div style="max-width: 400px;">
      <label style="
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #171717;
      ">
        Email Address
      </label>
      <input
        type="email"
        placeholder="you@example.com"
        style="
          ${inputBaseStyles}
          height: 40px;
          padding: 0 16px;
        "
        onfocus="
          this.style.borderColor = '#0ea5e9';
          this.style.boxShadow = '0 0 0 3px rgba(14, 165, 233, 0.3)';
        "
        onblur="
          this.style.borderColor = '#d4d4d4';
          this.style.boxShadow = 'none';
        "
        onmouseover="if (this !== document.activeElement) this.style.borderColor = '#a3a3a3'"
        onmouseout="if (this !== document.activeElement) this.style.borderColor = '#d4d4d4'"
      />
    </div>
  `,
};

export const Textarea = {
  render: () => `
    <div style="max-width: 400px;">
      <label style="
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #171717;
      ">
        Message
      </label>
      <textarea
        rows="4"
        placeholder="Enter your message here..."
        style="
          ${inputBaseStyles}
          padding: 16px;
          resize: vertical;
        "
        onfocus="
          this.style.borderColor = '#0ea5e9';
          this.style.boxShadow = '0 0 0 3px rgba(14, 165, 233, 0.3)';
        "
        onblur="
          this.style.borderColor = '#d4d4d4';
          this.style.boxShadow = 'none';
        "
        onmouseover="if (this !== document.activeElement) this.style.borderColor = '#a3a3a3'"
        onmouseout="if (this !== document.activeElement) this.style.borderColor = '#d4d4d4'"
      ></textarea>
    </div>
  `,
};

export const ErrorState = {
  render: () => `
    <div style="max-width: 400px;">
      <label style="
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #171717;
      ">
        Username
      </label>
      <input
        type="text"
        value="invalid-user"
        aria-invalid="true"
        style="
          ${inputBaseStyles}
          height: 40px;
          padding: 0 16px;
          border-color: #ef4444;
        "
        onfocus="
          this.style.borderColor = '#ef4444';
          this.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.2)';
        "
        onblur="
          this.style.borderColor = '#ef4444';
          this.style.boxShadow = 'none';
        "
      />
      <p style="
        margin-top: 8px;
        font-size: 14px;
        color: #ef4444;
      ">
        This username is already taken
      </p>
    </div>
  `,
};

export const SuccessState = {
  render: () => `
    <div style="max-width: 400px;">
      <label style="
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #171717;
      ">
        Email Address
      </label>
      <input
        type="email"
        value="user@example.com"
        style="
          ${inputBaseStyles}
          height: 40px;
          padding: 0 16px;
          border-color: #22c55e;
        "
        onfocus="
          this.style.borderColor = '#22c55e';
          this.style.boxShadow = '0 0 0 3px rgba(34, 197, 94, 0.2)';
        "
        onblur="
          this.style.borderColor = '#22c55e';
          this.style.boxShadow = 'none';
        "
      />
      <p style="
        margin-top: 8px;
        font-size: 14px;
        color: #22c55e;
      ">
        ✓ Email is available
      </p>
    </div>
  `,
};

export const DisabledState = {
  render: () => `
    <div style="max-width: 400px;">
      <label style="
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #a3a3a3;
      ">
        Disabled Input
      </label>
      <input
        type="text"
        value="Cannot edit this field"
        disabled
        style="
          ${inputBaseStyles}
          height: 40px;
          padding: 0 16px;
          background-color: #f5f5f5;
          color: #a3a3a3;
          cursor: not-allowed;
        "
      />
    </div>
  `,
};

export const InputSizes = {
  render: () => `
    <div style="max-width: 400px; display: flex; flex-direction: column; gap: 24px;">
      <div>
        <label style="display: block; margin-bottom: 8px; font-size: 12px; font-weight: 500; color: #171717;">
          Small (32px)
        </label>
        <input
          type="text"
          placeholder="Small input"
          style="
            ${inputBaseStyles}
            height: 32px;
            padding: 0 12px;
            font-size: 14px;
          "
        />
      </div>
      
      <div>
        <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500; color: #171717;">
          Medium (40px) - Default
        </label>
        <input
          type="text"
          placeholder="Medium input"
          style="
            ${inputBaseStyles}
            height: 40px;
            padding: 0 16px;
          "
        />
      </div>
      
      <div>
        <label style="display: block; margin-bottom: 8px; font-size: 16px; font-weight: 500; color: #171717;">
          Large (48px)
        </label>
        <input
          type="text"
          placeholder="Large input"
          style="
            ${inputBaseStyles}
            height: 48px;
            padding: 0 20px;
            font-size: 18px;
          "
        />
      </div>
    </div>
  `,
};

export const CompleteForm = {
  render: () => `
    <form style="max-width: 500px; background: white; padding: 32px; border-radius: 8px; border: 1px solid #e5e5e5;">
      <h2 style="font-size: 24px; font-weight: 700; margin: 0 0 24px 0; color: #171717;">
        Contact Form
      </h2>
      
      <div style="margin-bottom: 20px;">
        <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500; color: #171717;">
          Name *
        </label>
        <input
          type="text"
          required
          style="${inputBaseStyles} height: 40px; padding: 0 16px;"
          placeholder="Your name"
        />
      </div>
      
      <div style="margin-bottom: 20px;">
        <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500; color: #171717;">
          Email *
        </label>
        <input
          type="email"
          required
          style="${inputBaseStyles} height: 40px; padding: 0 16px;"
          placeholder="you@example.com"
        />
      </div>
      
      <div style="margin-bottom: 24px;">
        <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500; color: #171717;">
          Message *
        </label>
        <textarea
          rows="4"
          required
          style="${inputBaseStyles} padding: 16px; resize: vertical;"
          placeholder="Your message..."
        ></textarea>
      </div>
      
      <button
        type="submit"
        style="
          width: 100%;
          height: 48px;
          background-color: #0ea5e9;
          color: white;
          border: none;
          border-radius: 6px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.15s ease-out;
        "
        onmouseover="this.style.backgroundColor = '#0284c7'"
        onmouseout="this.style.backgroundColor = '#0ea5e9'"
      >
        Send Message
      </button>
    </form>
  `,
};
