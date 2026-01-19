export default {
  title: 'Components/Button',
  tags: ['autodocs'],
  argTypes: {
    label: { control: 'text' },
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'ghost'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
    disabled: { control: 'boolean' },
  },
  parameters: {
    docs: {
      description: {
        component: 'Buttons allow users to take actions with a single tap. Includes primary, secondary, and ghost variants.',
      },
    },
  },
};

const Template = ({ label, variant, size, disabled }) => {
  const variantStyles = {
    primary: `
      background-color: #0ea5e9;
      color: white;
      border: none;
    `,
    secondary: `
      background-color: transparent;
      color: #171717;
      border: 2px solid #d4d4d4;
    `,
    ghost: `
      background-color: transparent;
      color: #525252;
      border: none;
    `,
  };

  const sizeStyles = {
    sm: `
      height: 32px;
      padding: 0 16px;
      font-size: 14px;
    `,
    md: `
      height: 40px;
      padding: 0 24px;
      font-size: 16px;
    `,
    lg: `
      height: 48px;
      padding: 0 32px;
      font-size: 18px;
    `,
  };

  return `
    <button
      style="
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 600;
        border-radius: 6px;
        cursor: ${disabled ? 'not-allowed' : 'pointer'};
        transition: all 0.15s ease-out;
        opacity: ${disabled ? '0.5' : '1'};
        ${variantStyles[variant]}
        ${sizeStyles[size]}
      "
      ${disabled ? 'disabled' : ''}
      onmouseover="if (!this.disabled) { 
        if ('${variant}' === 'primary') this.style.backgroundColor = '#0284c7';
        if ('${variant}' === 'secondary') this.style.backgroundColor = '#f5f5f5';
        if ('${variant}' === 'ghost') this.style.backgroundColor = '#f5f5f5';
      }"
      onmouseout="if (!this.disabled) { 
        if ('${variant}' === 'primary') this.style.backgroundColor = '#0ea5e9';
        if ('${variant}' === 'secondary') this.style.backgroundColor = 'transparent';
        if ('${variant}' === 'ghost') this.style.backgroundColor = 'transparent';
      }"
    >
      ${label}
    </button>
  `;
};

export const Primary = {
  args: {
    label: 'Primary Button',
    variant: 'primary',
    size: 'md',
    disabled: false,
  },
  render: Template,
};

export const Secondary = {
  args: {
    label: 'Secondary Button',
    variant: 'secondary',
    size: 'md',
    disabled: false,
  },
  render: Template,
};

export const Ghost = {
  args: {
    label: 'Ghost Button',
    variant: 'ghost',
    size: 'md',
    disabled: false,
  },
  render: Template,
};

export const Small = {
  args: {
    label: 'Small Button',
    variant: 'primary',
    size: 'sm',
    disabled: false,
  },
  render: Template,
};

export const Large = {
  args: {
    label: 'Large Button',
    variant: 'primary',
    size: 'lg',
    disabled: false,
  },
  render: Template,
};

export const Disabled = {
  args: {
    label: 'Disabled Button',
    variant: 'primary',
    size: 'md',
    disabled: true,
  },
  render: Template,
};

export const AllVariants = {
  render: () => `
    <div style="display: flex; gap: 16px; flex-wrap: wrap; align-items: center;">
      ${Template({ label: 'Primary', variant: 'primary', size: 'md', disabled: false })}
      ${Template({ label: 'Secondary', variant: 'secondary', size: 'md', disabled: false })}
      ${Template({ label: 'Ghost', variant: 'ghost', size: 'md', disabled: false })}
    </div>
  `,
};

export const AllSizes = {
  render: () => `
    <div style="display: flex; gap: 16px; align-items: center;">
      ${Template({ label: 'Small', variant: 'primary', size: 'sm', disabled: false })}
      ${Template({ label: 'Medium', variant: 'primary', size: 'md', disabled: false })}
      ${Template({ label: 'Large', variant: 'primary', size: 'lg', disabled: false })}
    </div>
  `,
};

export const IconButton = {
  render: () => `
    <button
      style="
        width: 40px;
        height: 40px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: transparent;
        border: none;
        border-radius: 9999px;
        cursor: pointer;
        transition: background-color 0.15s ease-out;
        color: #525252;
      "
      aria-label="Close"
      onmouseover="this.style.backgroundColor = '#f5f5f5'"
      onmouseout="this.style.backgroundColor = 'transparent'"
    >
      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" />
      </svg>
    </button>
  `,
};
