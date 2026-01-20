export default {
  title: 'Components/Hero Section',
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Large hero section with centered content, title, subtitle, and decorative image. Used on homepage for immediate impact.',
      },
    },
    layout: 'fullscreen',
  },
};

const Template = ({ title, subtitle, imageUrl, imageAlt }) => {
  return `
    <section style="
      padding: 80px 24px;
      background: linear-gradient(180deg, #fafafa 0%, #ffffff 100%);
      text-align: center;
      min-height: 60vh;
      display: flex;
      align-items: center;
      justify-content: center;
    ">
      <div style="
        max-width: 640px;
        margin: 0 auto;
      ">
        <h1 style="
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: clamp(2.25rem, 1.5rem + 3.75vw, 4.5rem);
          font-weight: 700;
          color: #171717;
          margin: 0 0 16px 0;
          line-height: 1.1;
        ">
          ${title}
        </h1>
        
        <p style="
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
          color: #525252;
          margin: 0 0 48px 0;
          line-height: 1.625;
        ">
          ${subtitle}
        </p>
        
        ${imageUrl ? `
          <div style="
            position: relative;
            max-width: 420px;
            margin: 0 auto;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.3s ease-out;
          "
          onmouseover="this.style.transform = 'scale(1.02)'"
          onmouseout="this.style.transform = 'scale(1)'">
            <img 
              src="${imageUrl}" 
              alt="${imageAlt}"
              style="
                width: 100%;
                height: auto;
                display: block;
              "
            />
          </div>
        ` : ''}
      </div>
    </section>
  `;
};

export const Default = {
  args: {
    title: 'Hello, World!',
    subtitle: 'Personal website intended as a learning project.',
    imageUrl: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=450&fit=crop',
    imageAlt: 'Decorative jellyfish in dark water with pink and purple lighting',
  },
  render: Template,
};

export const WithoutImage = {
  args: {
    title: 'Hello, World!',
    subtitle: 'Personal website intended as a learning project.',
    imageUrl: '',
    imageAlt: '',
  },
  render: Template,
};

export const LongSubtitle = {
  args: {
    title: 'Hello, World!',
    subtitle: 'Personal website intended as a learning project. This site showcases my work, skills, and journey as a developer building products that solve real problems.',
    imageUrl: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=450&fit=crop',
    imageAlt: 'Decorative jellyfish in dark water',
  },
  render: Template,
};

export const CustomContent = {
  args: {
    title: 'Welcome to My Portfolio',
    subtitle: 'Building products that solve real problems.',
    imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&h=450&fit=crop',
    imageAlt: 'Abstract colorful gradient',
  },
  render: Template,
};

export const MobileView = {
  args: {
    title: 'Hello, World!',
    subtitle: 'Personal website intended as a learning project.',
    imageUrl: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=450&fit=crop',
    imageAlt: 'Decorative jellyfish',
  },
  render: Template,
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
