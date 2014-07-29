var config = {
  programs: [
    "melt",
    "sparkle",
    "melt sparkle",
    "test",
    "fadeout",
    "red"
  ],
  schedules: [
    {
      name: "main",
      shows: [
        {
          program: 'melt',
          length: 1200
        },
        {
          program: 'melt sparkle',
          length: 1200
        }
      ]
    }
  ]
}
