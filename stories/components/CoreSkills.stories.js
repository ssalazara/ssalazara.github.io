export default {
  title: 'Components/Core Skills',
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Displays core skills as pill-style tags in a centered, responsive layout. Skills are clickable and have hover effects.',
      },
    },
  },
};

const Template = ({ skills, title }) => {
  return `
    <section style="
      padding: 64px 24px;
      background-color: #fafafa;
    ">
      <div style="
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
      ">
        <h2 style="
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: clamp(1.875rem, 1.5rem + 1.875vw, 2.25rem);
          font-weight: 700;
          color: #171717;
          margin: 0 0 32px 0;
        ">
          ${title}
        </h2>
        
        <div style="
          display: flex;
          flex-wrap: wrap;
          gap: 16px;
          justify-content: center;
          align-items: center;
        ">
          ${skills.map(skill => `
            <span style="
              display: inline-block;
              padding: 12px 24px;
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              font-size: 16px;
              font-weight: 500;
              color: #525252;
              background-color: #ffffff;
              border: 1px solid #e5e5e5;
              border-radius: 9999px;
              cursor: pointer;
              transition: all 0.15s ease-out;
              white-space: nowrap;
            "
            onmouseover="
              this.style.backgroundColor = '#f0f9ff';
              this.style.borderColor = '#0ea5e9';
              this.style.color = '#0369a1';
            "
            onmouseout="
              this.style.backgroundColor = '#ffffff';
              this.style.borderColor = '#e5e5e5';
              this.style.color = '#525252';
            ">
              ${skill}
            </span>
          `).join('')}
        </div>
      </div>
    </section>
  `;
};

export const Default = {
  args: {
    title: 'Core Skills',
    skills: [
      'Problem Solving',
      'Content Strategy',
      'Data Science',
      'Headless CMS',
    ],
  },
  render: Template,
};

export const TechnicalSkills = {
  args: {
    title: 'Technical Skills',
    skills: [
      'JavaScript',
      'Python',
      'React',
      'Node.js',
      'PostgreSQL',
      'AWS',
    ],
  },
  render: Template,
};

export const MinimalSkills = {
  args: {
    title: 'What I Do',
    skills: [
      'Design',
      'Development',
      'Strategy',
    ],
  },
  render: Template,
};

export const ManySkills = {
  args: {
    title: 'Skills & Expertise',
    skills: [
      'Problem Solving',
      'Content Strategy',
      'Data Science',
      'Headless CMS',
      'JavaScript',
      'Python',
      'React',
      'Node.js',
      'PostgreSQL',
      'AWS',
      'Docker',
      'CI/CD',
    ],
  },
  render: Template,
};

export const MobileView = {
  args: {
    title: 'Core Skills',
    skills: [
      'Problem Solving',
      'Content Strategy',
      'Data Science',
      'Headless CMS',
    ],
  },
  render: Template,
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};

export const CustomTitle = {
  args: {
    title: 'My Superpowers',
    skills: [
      'Problem Solving',
      'Content Strategy',
      'Data Science',
      'Headless CMS',
    ],
  },
  render: Template,
};
