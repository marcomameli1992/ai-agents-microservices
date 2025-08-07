class AnalysisResult {
  final String url;
  final Map<String, dynamic> extractedData;

  AnalysisResult({required this.url, required this.extractedData});

  factory AnalysisResult.fromJson(Map<String, dynamic> json) {
    return AnalysisResult(
      url: json['url'] ?? '',
      extractedData: json['extracted_data'] ?? {},
    );
  }
}
