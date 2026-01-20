export default {
  title: 'Components/Featured Projects',
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Displays featured projects in a responsive 2-column grid. Each project card includes an image, title, description, and CTA link.',
      },
    },
  },
};

const ProjectCard = ({ title, description, imageUrl, linkUrl, linkText }) => `
  <article style="
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease-out;
    cursor: pointer;
  "
  onmouseover="
    this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
    this.style.transform = 'translateY(-4px)';
  "
  onmouseout="
    this.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
    this.style.transform = 'translateY(0)';
  ">
    <!-- Project Image -->
    <div style="
      width: 100%;
      aspect-ratio: 16 / 9;
      overflow: hidden;
      background-color: #f5f5f5;
    ">
      ${imageUrl ? `
        <img 
          src="${imageUrl}" 
          alt="${title}"
          style="
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
          "
        />
      ` : `
        <div style="
          width: 100%;
          height: 100%;
          background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        "></div>
      `}
    </div>
    
    <!-- Project Content -->
    <div style="padding: 24px;">
      <h3 style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #171717;
        margin: 0 0 12px 0;
        line-height: 1.25;
      ">
        ${title}
      </h3>
      
      <p style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 16px;
        line-height: 1.625;
        color: #525252;
        margin: 0 0 20px 0;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
      ">
        ${description}
      </p>
      
      <a 
        href="${linkUrl}" 
        style="
          display: inline-flex;
          align-items: center;
          gap: 8px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: 16px;
          font-weight: 600;
          color: #0284c7;
          text-decoration: none;
          transition: color 0.15s ease-out;
        "
        onmouseover="this.style.color = '#0369a1'"
        onmouseout="this.style.color = '#0284c7'"
      >
        ${linkText}
        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </a>
    </div>
  </article>
`;

const Template = ({ title, projects }) => {
  return `
    <section style="
      padding: 64px 24px;
      background-color: #ffffff;
    ">
      <div style="
        max-width: 1200px;
        margin: 0 auto;
      ">
        <h2 style="
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: clamp(1.875rem, 1.5rem + 1.875vw, 2.25rem);
          font-weight: 700;
          color: #171717;
          margin: 0 0 48px 0;
          text-align: center;
        ">
          ${title}
        </h2>
        
        <div style="
          display: grid;
          grid-template-columns: 1fr;
          gap: 32px;
        ">
          ${projects.map(project => ProjectCard(project)).join('')}
        </div>
      </div>
    </section>
    
    <style>
      @media (min-width: 768px) {
        section > div > div {
          grid-template-columns: repeat(2, 1fr);
        }
      }
    </style>
  `;
};

export const Default = {
  args: {
    title: 'Featured Projects',
    projects: [
      {
        title: 'My Personal Profile',
        description: 'Self-taught project based on using a free tech-stack for a personal website. In short: Astro + Sanity + Netlify',
        imageUrl: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=450&fit=crop',
        linkUrl: 'https://simonsalazar.netlify.app/',
        linkText: 'View Project',
      },
      {
        title: 'Rosetta Bridge',
        description: 'Part of the winning team at the Apply Digital hackathon in July 2025. Rosetta Bridge is an agent-based solution that utilizes a JSON object to generate user-friendly documentation based on the specified requirements.',
        imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=450&fit=crop',
        linkUrl: '#',
        linkText: 'View Project',
      },
    ],
  },
  render: Template,
};

export const ThreeProjects = {
  args: {
    title: 'Featured Projects',
    projects: [
      {
        title: 'E-Commerce Platform',
        description: 'Built a full-stack e-commerce platform with React, Node.js, and PostgreSQL. Features include user authentication, product catalog, shopping cart, and payment integration.',
        imageUrl: 'https://images.unsplash.com/photo-1557821552-17105176677c?w=800&h=450&fit=crop',
        linkUrl: '#',
        linkText: 'View Project',
      },
      {
        title: 'Data Visualization Dashboard',
        description: 'Interactive dashboard for visualizing complex datasets using D3.js and React. Real-time updates and responsive design for mobile and desktop.',
        imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=450&fit=crop',
        linkUrl: '#',
        linkText: 'View Project',
      },
      {
        title: 'Mobile App',
        description: 'Cross-platform mobile application built with React Native. Features offline support, push notifications, and seamless synchronization.',
        imageUrl: 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&h=450&fit=crop',
        linkUrl: '#',
        linkText: 'View Project',
      },
    ],
  },
  render: Template,
};

export const WithoutImages = {
  args: {
    title: 'Featured Projects',
    projects: [
      {
        title: 'My Personal Profile',
        description: 'Self-taught project based on using a free tech-stack for a personal website. In short: Astro + Sanity + Netlify',
        imageUrl: '',
        linkUrl: 'https://simonsalazar.netlify.app/',
        linkText: 'View Project',
      },
      {
        title: 'Rosetta Bridge',
        description: 'Part of the winning team at the Apply Digital hackathon in July 2025. Rosetta Bridge is an agent-based solution.',
        imageUrl: '',
        linkUrl: '#',
        linkText: 'View Project',
      },
    ],
  },
  render: Template,
};

export const SingleProject = {
  args: {
    title: 'Featured Work',
    projects: [
      {
        title: 'My Personal Profile',
        description: 'Self-taught project based on using a free tech-stack for a personal website. In short: Astro + Sanity + Netlify',
        imageUrl: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=450&fit=crop',
        linkUrl: 'https://simonsalazar.netlify.app/',
        linkText: 'View Project',
      },
    ],
  },
  render: Template,
};

export const MobileView = {
  args: {
    title: 'Featured Projects',
    projects: [
      {
        title: 'My Personal Profile',
        description: 'Self-taught project based on using a free tech-stack for a personal website.',
        imageUrl: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=450&fit=crop',
        linkUrl: '#',
        linkText: 'View Project',
      },
      {
        title: 'Rosetta Bridge',
        description: 'Winning hackathon team solution that generates user-friendly documentation.',
        imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=450&fit=crop',
        linkUrl: '#',
        linkText: 'View Project',
      },
    ],
  },
  render: Template,
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
