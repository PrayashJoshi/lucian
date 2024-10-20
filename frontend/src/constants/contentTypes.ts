// src/constants/contentTypes.ts
export const ContentTypes = {
    NONE: 'none',
    ONE: 'one',
    TWO: 'two',
  } as const;
  
  export type ContentType = typeof ContentTypes[keyof typeof ContentTypes];
  