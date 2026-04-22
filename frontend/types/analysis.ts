export type AnalyzeRequest = {
  content: string;
};

export type AnalyzeResponse = {
  score: number;
  label: string;
  reasons: string[];
};
