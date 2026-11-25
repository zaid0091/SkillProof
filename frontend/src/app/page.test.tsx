import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import Home from './page';

describe('SkillProof landing page', () => {
  it('presents the verified evidence workflow', () => {
    render(<Home />);
    expect(screen.getByRole('heading', { name: /proof over promises/i })).toBeInTheDocument();
    expect(screen.getByText(/4 evidence layers/i)).toBeInTheDocument();
  });
});
