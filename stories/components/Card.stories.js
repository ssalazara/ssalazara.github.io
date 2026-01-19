export default {
  title: 'Components/Card',
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Cards are flexible containers for grouping related content. Includes blog post card variant with image, title, excerpt, and metadata.',
      },
    },
  },
};

export const BasicCard = {
  render: () => `
    <div style="
      padding: 24px;
      background-color: white;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
      max-width: 400px;
    ">
      <h3 style="font-size: 20px; font-weight: 700; margin: 0 0 12px 0; color: #171717;">
        Card Title
      </h3>
      <p style="font-size: 16px; line-height: 1.5; color: #525252; margin: 0;">
        This is a basic card component with title and content. Cards are flexible containers for grouping related information.
      </p>
    </div>
  `,
};

export const BlogPostCard = {
  render: () => `
    <article style="
      display: flex;
      flex-direction: column;
      background-color: white;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
      max-width: 360px;
      overflow: hidden;
      transition: box-shadow 0.25s ease-out, transform 0.25s ease-out;
      cursor: pointer;
    "
    onmouseover="
      this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
      this.style.transform = 'translateY(-2px)';
    "
    onmouseout="
      this.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
      this.style.transform = 'translateY(0)';
    "
    >
      <div style="
        width: 100%;
        aspect-ratio: 16 / 9;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
      "></div>
      <div style="padding: 24px;">
        <h3 style="
          font-size: 20px;
          font-weight: 700;
          margin: 0 0 12px 0;
          color: #171717;
          line-height: 1.25;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        ">
          Understanding Modern Design Systems
        </h3>
        <p style="
          font-size: 14px;
          line-height: 1.625;
          color: #525252;
          margin: 0 0 16px 0;
          display: -webkit-box;
          -webkit-line-clamp: 3;
          -webkit-box-orient: vertical;
          overflow: hidden;
        ">
          A comprehensive guide to building scalable and maintainable design systems that work across platforms and teams.
        </p>
        <div style="
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 12px;
          color: #737373;
          margin-bottom: 16px;
        ">
          <time datetime="2026-01-19">January 19, 2026</time>
          <span style="
            padding: 4px 8px;
            background-color: #f0f9ff;
            color: #0369a1;
            border-radius: 4px;
            font-weight: 500;
          ">Design</span>
        </div>
        <a href="#" style="
          color: #0284c7;
          font-weight: 600;
          text-decoration: none;
          font-size: 14px;
        ">Read more →</a>
      </div>
    </article>
  `,
};

export const BlogPostGrid = {
  render: () => `
    <div style="
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 24px;
      max-width: 1200px;
    ">
      ${[1, 2, 3].map(i => `
        <article style="
          display: flex;
          flex-direction: column;
          background-color: white;
          border: 1px solid #e5e5e5;
          border-radius: 8px;
          box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
          overflow: hidden;
          transition: box-shadow 0.25s ease-out, transform 0.25s ease-out;
          cursor: pointer;
        "
        onmouseover="
          this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
          this.style.transform = 'translateY(-2px)';
        "
        onmouseout="
          this.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
          this.style.transform = 'translateY(0)';
        "
        >
          <div style="
            width: 100%;
            aspect-ratio: 16 / 9;
            background: linear-gradient(${135 + i * 30}deg, #0ea5e9 0%, #0284c7 100%);
          "></div>
          <div style="padding: 24px;">
            <h3 style="
              font-size: 20px;
              font-weight: 700;
              margin: 0 0 12px 0;
              color: #171717;
              line-height: 1.25;
            ">
              Blog Post Title ${i}
            </h3>
            <p style="
              font-size: 14px;
              line-height: 1.625;
              color: #525252;
              margin: 0 0 16px 0;
            ">
              A brief excerpt from the blog post that gives readers a preview of the content...
            </p>
            <div style="
              display: flex;
              align-items: center;
              gap: 12px;
              font-size: 12px;
              color: #737373;
            ">
              <time>Jan ${19 + i}, 2026</time>
              <span style="
                padding: 4px 8px;
                background-color: #f0f9ff;
                color: #0369a1;
                border-radius: 4px;
                font-weight: 500;
              ">${['Design', 'Tech', 'Lifestyle'][i - 1]}</span>
            </div>
          </div>
        </article>
      `).join('')}
    </div>
  `,
};

export const InteractiveCard = {
  render: () => `
    <div style="
      padding: 24px;
      background-color: white;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
      max-width: 400px;
      cursor: pointer;
      transition: box-shadow 0.25s ease-out, transform 0.25s ease-out;
    "
    onmouseover="
      this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
      this.style.transform = 'translateY(-2px)';
    "
    onmouseout="
      this.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
      this.style.transform = 'translateY(0)';
    "
    >
      <h3 style="font-size: 20px; font-weight: 700; margin: 0 0 12px 0; color: #171717;">
        Interactive Card
      </h3>
      <p style="font-size: 16px; line-height: 1.5; color: #525252; margin: 0;">
        Hover over this card to see the elevation effect. The card smoothly lifts on hover with a subtle shadow.
      </p>
    </div>
  `,
};
