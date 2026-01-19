export default {
  title: 'Foundation/Typography',
  parameters: {
    docs: {
      description: {
        component: 'Typography system with fluid responsive scaling. Includes Inter for UI, Merriweather for headings.',
      },
    },
  },
};

export const TypeScale = {
  render: () => `
    <div style="max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      <div style="margin-bottom: 48px;">
        <h1 style="font-size: clamp(3rem, 2.25rem + 3.75vw, 3.75rem); font-weight: 700; line-height: 1.25; margin-bottom: 8px; color: #171717;">
          Display XL (48-60px)
        </h1>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(3rem, 2.25rem + 3.75vw, 3.75rem)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <h1 style="font-size: clamp(2.25rem, 1.8rem + 2.25vw, 3rem); font-weight: 700; line-height: 1.25; margin-bottom: 8px; color: #171717;">
          Display Large (36-48px)
        </h1>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(2.25rem, 1.8rem + 2.25vw, 3rem)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <h2 style="font-size: clamp(1.875rem, 1.5rem + 1.875vw, 2.25rem); font-weight: 700; line-height: 1.375; margin-bottom: 8px; color: #171717;">
          Heading 1 (30-36px)
        </h2>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(1.875rem, 1.5rem + 1.875vw, 2.25rem)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <h3 style="font-size: clamp(1.5rem, 1.3rem + 1vw, 1.875rem); font-weight: 700; line-height: 1.375; margin-bottom: 8px; color: #171717;">
          Heading 2 (24-30px)
        </h3>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(1.5rem, 1.3rem + 1vw, 1.875rem)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <h4 style="font-size: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem); font-weight: 600; line-height: 1.5; margin-bottom: 8px; color: #171717;">
          Heading 3 (20-24px)
        </h4>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <p style="font-size: clamp(1.125rem, 1rem + 0.625vw, 1.25rem); font-weight: 400; line-height: 1.625; margin-bottom: 8px; color: #171717;">
          Body Large (18-20px) - Used for lead paragraphs and important content that needs emphasis.
        </p>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(1.125rem, 1rem + 0.625vw, 1.25rem)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <p style="font-size: 1rem; font-weight: 400; line-height: 1.5; margin-bottom: 8px; color: #525252;">
          Body (16px) - Default body text size. Optimal for readability and used for most content throughout the site.
        </p>
        <p style="color: #737373; font-size: 14px;">font-size: 1rem (16px)</p>
      </div>
      
      <div style="margin-bottom: 48px;">
        <p style="font-size: clamp(0.875rem, 0.8rem + 0.375vw, 0.9375rem); font-weight: 400; line-height: 1.5; margin-bottom: 8px; color: #525252;">
          Body Small (14-15px) - Used for metadata, captions, and secondary information.
        </p>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(0.875rem, 0.8rem + 0.375vw, 0.9375rem)</p>
      </div>
      
      <div>
        <p style="font-size: clamp(0.75rem, 0.7rem + 0.25vw, 0.8125rem); font-weight: 400; line-height: 1.5; margin-bottom: 8px; color: #737373;">
          Caption (12-13px) - Used for very small text like timestamps and labels.
        </p>
        <p style="color: #737373; font-size: 14px;">font-size: clamp(0.75rem, 0.7rem + 0.25vw, 0.8125rem)</p>
      </div>
    </div>
  `,
};

export const FontWeights = {
  render: () => `
    <div style="max-width: 700px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      <div style="margin-bottom: 24px;">
        <p style="font-size: 18px; font-weight: 300; color: #171717; margin-bottom: 4px;">
          Light (300) - Rarely used
        </p>
      </div>
      <div style="margin-bottom: 24px;">
        <p style="font-size: 18px; font-weight: 400; color: #171717; margin-bottom: 4px;">
          Normal (400) - Body text
        </p>
      </div>
      <div style="margin-bottom: 24px;">
        <p style="font-size: 18px; font-weight: 500; color: #171717; margin-bottom: 4px;">
          Medium (500) - Subtle emphasis
        </p>
      </div>
      <div style="margin-bottom: 24px;">
        <p style="font-size: 18px; font-weight: 600; color: #171717; margin-bottom: 4px;">
          Semibold (600) - Strong emphasis, links
        </p>
      </div>
      <div style="margin-bottom: 24px;">
        <p style="font-size: 18px; font-weight: 700; color: #171717; margin-bottom: 4px;">
          Bold (700) - Headings, CTAs
        </p>
      </div>
      <div>
        <p style="font-size: 18px; font-weight: 800; color: #171717; margin-bottom: 4px;">
          Extrabold (800) - Display headings
        </p>
      </div>
    </div>
  `,
};

export const LineHeights = {
  render: () => `
    <div style="max-width: 700px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      <div style="margin-bottom: 32px;">
        <h3 style="font-size: 24px; line-height: 1.25; margin-bottom: 8px; color: #171717;">
          Tight (1.25) - Large headings
        </h3>
        <p style="color: #737373; font-size: 14px;">Used for H1, H2, and display text</p>
      </div>
      
      <div style="margin-bottom: 32px;">
        <p style="font-size: 16px; line-height: 1.375; margin-bottom: 8px; color: #171717;">
          Snug (1.375) - Subheadings. Provides compact spacing for headings that need better density.
        </p>
        <p style="color: #737373; font-size: 14px;">Used for H3, H4</p>
      </div>
      
      <div style="margin-bottom: 32px;">
        <p style="font-size: 16px; line-height: 1.5; margin-bottom: 8px; color: #171717;">
          Normal (1.5) - Body text. The default line height for most content. Provides good readability without excessive spacing.
        </p>
        <p style="color: #737373; font-size: 14px;">Used for standard body text</p>
      </div>
      
      <div style="margin-bottom: 32px;">
        <p style="font-size: 16px; line-height: 1.625; margin-bottom: 8px; color: #171717;">
          Relaxed (1.625) - Long-form content. Ideal for blog posts and articles where you want readers to have an easier time following lines of text. The increased spacing improves readability for extended reading sessions.
        </p>
        <p style="color: #737373; font-size: 14px;">Used for blog post content</p>
      </div>
      
      <div>
        <p style="font-size: 14px; line-height: 2; margin-bottom: 8px; color: #171717;">
          Loose (2.0) - Captions and labels. Very spacious line height used for small text that needs extra breathing room, like form labels or image captions.
        </p>
        <p style="color: #737373; font-size: 14px;">Used for captions, labels</p>
      </div>
    </div>
  `,
};
