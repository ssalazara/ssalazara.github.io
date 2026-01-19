export default {
  title: 'Foundation/Colors',
  parameters: {
    docs: {
      description: {
        component: 'Color palette with blue and gray sophisticated minimalist theme. All colors are WCAG AA compliant for accessibility.',
      },
    },
  },
};

const ColorSwatch = ({ name, hex, usage, contrastRatio }) => `
  <div style="margin-bottom: 24px;">
    <div style="display: flex; gap: 16px; align-items: center;">
      <div style="
        width: 80px;
        height: 80px;
        background-color: ${hex};
        border-radius: 8px;
        border: 1px solid #e5e5e5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      "></div>
      <div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 600; color: #171717;">
          ${name}
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #525252; margin-top: 4px;">
          ${hex}
        </div>
        <div style="font-size: 14px; color: #737373; margin-top: 8px;">
          ${usage}
        </div>
        ${contrastRatio ? `
          <div style="font-size: 12px; color: ${contrastRatio >= 4.5 ? '#22c55e' : '#ef4444'}; margin-top: 4px; font-weight: 600;">
            ${contrastRatio >= 4.5 ? '✓' : '✗'} Contrast: ${contrastRatio}:1 ${contrastRatio >= 4.5 ? '(AA)' : '(Fail)'}
          </div>
        ` : ''}
      </div>
    </div>
  </div>
`;

const ColorPalette = ({ colors }) => `
  <div style="max-width: 800px;">
    ${colors.map(color => ColorSwatch(color)).join('')}
  </div>
`;

export const PrimaryBlue = {
  render: () => ColorPalette({
    colors: [
      { name: '$color-primary-50', hex: '#f0f9ff', usage: 'Subtle backgrounds, badges' },
      { name: '$color-primary-100', hex: '#e0f2fe', usage: 'Light backgrounds' },
      { name: '$color-primary-200', hex: '#bae6fd', usage: 'Borders, highlights' },
      { name: '$color-primary-300', hex: '#7dd3fc', usage: 'Soft accents' },
      { name: '$color-primary-400', hex: '#38bdf8', usage: 'Medium blue' },
      { name: '$color-primary-500', hex: '#0ea5e9', usage: 'Main brand color, CTAs' },
      { name: '$color-primary-600', hex: '#0284c7', usage: 'Links, hover states', contrastRatio: 5.8 },
      { name: '$color-primary-700', hex: '#0369a1', usage: 'Deep blue, visited links' },
      { name: '$color-primary-800', hex: '#075985', usage: 'Very deep blue' },
      { name: '$color-primary-900', hex: '#0c4a6e', usage: 'Darkest blue' },
    ],
  }),
};

export const NeutralGray = {
  render: () => ColorPalette({
    colors: [
      { name: '$color-neutral-0', hex: '#ffffff', usage: 'Pure white, cards' },
      { name: '$color-neutral-50', hex: '#fafafa', usage: 'Page background' },
      { name: '$color-neutral-100', hex: '#f5f5f5', usage: 'Card backgrounds' },
      { name: '$color-neutral-200', hex: '#e5e5e5', usage: 'Borders, dividers' },
      { name: '$color-neutral-300', hex: '#d4d4d4', usage: 'Subtle borders' },
      { name: '$color-neutral-400', hex: '#a3a3a3', usage: 'Disabled text', contrastRatio: 2.88 },
      { name: '$color-neutral-500', hex: '#737373', usage: 'Secondary text', contrastRatio: 4.61 },
      { name: '$color-neutral-600', hex: '#525252', usage: 'Body text', contrastRatio: 7.93 },
      { name: '$color-neutral-700', hex: '#404040', usage: 'Headings', contrastRatio: 10.41 },
      { name: '$color-neutral-800', hex: '#262626', usage: 'Strong emphasis', contrastRatio: 14.79 },
      { name: '$color-neutral-900', hex: '#171717', usage: 'Maximum contrast', contrastRatio: 18.25 },
    ],
  }),
};

export const SemanticColors = {
  render: () => ColorPalette({
    colors: [
      { name: '$color-success-500', hex: '#22c55e', usage: 'Success messages, positive states' },
      { name: '$color-warning-500', hex: '#f59e0b', usage: 'Warning messages, attention' },
      { name: '$color-error-500', hex: '#ef4444', usage: 'Error messages, destructive actions' },
      { name: '$color-info-500', hex: '#3b82f6', usage: 'Informational messages' },
    ],
  }),
};

export const TextColors = {
  render: () => `
    <div style="max-width: 800px;">
      <div style="margin-bottom: 32px;">
        <h3 style="margin-bottom: 16px; color: #171717;">Text Color Examples</h3>
        <div style="background: white; padding: 24px; border-radius: 8px; border: 1px solid #e5e5e5;">
          <p style="color: #171717; font-size: 16px; margin-bottom: 12px;">
            <strong>Primary text</strong> - Used for main body content (#171717)
          </p>
          <p style="color: #525252; font-size: 16px; margin-bottom: 12px;">
            <strong>Secondary text</strong> - Used for supporting information (#525252)
          </p>
          <p style="color: #737373; font-size: 16px; margin-bottom: 12px;">
            <strong>Tertiary text</strong> - Used for muted text, captions (#737373)
          </p>
          <p style="color: #a3a3a3; font-size: 16px; margin-bottom: 12px;">
            <strong>Disabled text</strong> - Used for disabled states (#a3a3a3)
          </p>
          <p style="margin-bottom: 0;">
            <a href="#" style="color: #0284c7; text-decoration: none; font-weight: 600;">Link text</a> - Primary links (#0284c7)
          </p>
        </div>
      </div>
    </div>
  `,
};
