"""Cross-cutting helpers shared by every domain module.

Nothing here owns business data. This package holds the API error envelope,
base model classes, pagination, permission primitives, health checks, and
infrastructure tasks so that each domain module stays small.
"""
