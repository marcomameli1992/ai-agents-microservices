class SearchResult {
  final String url;
  final String title;
  final String snippet;

  SearchResult({required this.url, required this.title, required this.snippet});

  factory SearchResult.fromJson(Map<String, dynamic> json) {
    return SearchResult(
      url: json['url'] ?? '',
      title: json['title'] ?? '',
      snippet: json['snippet'] ?? '',
    );
  }
}
