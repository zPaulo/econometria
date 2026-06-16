'use client';
import { useState } from 'react';

export default function GlossaryTooltip({ text, glossary }) {
  if (!text || !glossary || glossary.length === 0) return <span>{text}</span>;

  // Create a regex to match any of the glossary terms
  const terms = glossary.map(g => g.term);
  // Sort by length descending to match longest terms first
  terms.sort((a, b) => b.length - a.length);
  
  const regexStr = `\\b(${terms.join('|')})\\b`;
  const regex = new RegExp(regexStr, 'gi');

  const parts = text.split(regex);

  return (
    <span>
      {parts.map((part, index) => {
        const isTerm = terms.some(t => t.toLowerCase() === part.toLowerCase());
        
        if (isTerm) {
          const def = glossary.find(g => g.term.toLowerCase() === part.toLowerCase())?.definition;
          return (
            <TooltipWrapper key={index} term={part} definition={def} />
          );
        }
        return <span key={index}>{part}</span>;
      })}
    </span>
  );
}

function TooltipWrapper({ term, definition }) {
  const [show, setShow] = useState(false);

  return (
    <span 
      style={{ position: 'relative', cursor: 'pointer', borderBottom: '1px dashed var(--text-highlight)', color: 'var(--text-highlight)' }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
    >
      {term}
      {show && (
        <span 
          className="tooltip-content glass-panel"
          style={{
            position: 'absolute',
            bottom: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            marginBottom: '8px',
            width: '250px',
            padding: '12px',
            zIndex: 10,
            fontSize: '0.9rem',
            color: '#fff',
            fontWeight: 'normal',
            lineHeight: '1.4'
          }}
        >
          <strong style={{ color: 'var(--text-highlight)' }}>{term}</strong>: {definition}
        </span>
      )}
    </span>
  );
}
