# Adapted from the "ci/build-android" branch of https://github.com/qfeng3168/TV
# (.github/workflows/android-build.yml, commits 26d33af, 97ca285 and 87ba974).
# FongMi/TV and derivatives are licensed under the GNU GPL v3; see LICENSE.md.

# Run from the directory that holds the FongMi/media checkout at ./media.
import pathlib
import sys

ROOT = pathlib.Path("media/libraries/mpvplayer/src/main/java/androidx/media3/mpvplayer")


def patch(relative, *replacements):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    before = (text.count("{"), text.count("}"))
    for old, new in replacements:
        occurrences = text.count(old)
        if occurrences != 1:
            print("::error::" + relative + ": anchor matched "
                  + str(occurrences) + " times, expected exactly 1")
            print(old)
            sys.exit(1)
        text = text.replace(old, new)
    after = (text.count("{"), text.count("}"))
    added = (after[0] - before[0], after[1] - before[1])
    if added[0] != added[1] or added[0] == 0:
        print("::error::" + relative + ": patch added unbalanced braces " + str(added))
        sys.exit(1)
    path.write_text(text, encoding="utf-8")
    print("patched " + relative + " (+" + str(added[0]) + " blocks)")


patch(
    "MpvSubtitleOptions.java",
    (
        "import androidx.annotation.RestrictTo;\n"
        "import com.google.errorprone.annotations.CanIgnoreReturnValue;\n",
        "import androidx.annotation.Nullable;\n"
        "import androidx.annotation.RestrictTo;\n"
        "import com.google.errorprone.annotations.CanIgnoreReturnValue;\n",
    ),
    (
        "  private final boolean secondaryOverrideAssStyles;\n"
        "\n"
        "  private MpvSubtitleOptions(Builder builder) {\n",
        "  private final boolean secondaryOverrideAssStyles;\n"
        "  @Nullable private final String fontFamily;\n"
        "  @Nullable private final String fontsDirectory;\n"
        "\n"
        "  private MpvSubtitleOptions(Builder builder) {\n",
    ),
    (
        "    secondaryOverrideAssStyles = builder.secondaryOverrideAssStyles;\n"
        "  }\n",
        "    secondaryOverrideAssStyles = builder.secondaryOverrideAssStyles;\n"
        "    fontFamily = builder.fontFamily;\n"
        "    fontsDirectory = builder.fontsDirectory;\n"
        "  }\n",
    ),
    (
        "  /** Builder for {@link MpvSubtitleOptions}. */\n"
        "  public static final class Builder {\n",
        "  /**\n"
        "   * Returns the font family to render subtitles with, or {@code null} to let the player\n"
        "   * choose one.\n"
        "   */\n"
        "  public @Nullable String getFontFamily() {\n"
        "    return fontFamily;\n"
        "  }\n"
        "\n"
        "  /** Returns the directory to load subtitle fonts from, or {@code null} for the default. */\n"
        "  public @Nullable String getFontsDirectory() {\n"
        "    return fontsDirectory;\n"
        "  }\n"
        "\n"
        "  /** Builder for {@link MpvSubtitleOptions}. */\n"
        "  public static final class Builder {\n",
    ),
    (
        "    private boolean secondaryOverrideAssStyles;\n"
        "    private boolean buildCalled;\n",
        "    private boolean secondaryOverrideAssStyles;\n"
        "    @Nullable private String fontFamily;\n"
        "    @Nullable private String fontsDirectory;\n"
        "    private boolean buildCalled;\n",
    ),
    (
        "    public MpvSubtitleOptions build() {\n",
        "    /** Sets the font family used to render subtitles. */\n"
        "    @CanIgnoreReturnValue\n"
        "    public Builder setFontFamily(String fontFamily) {\n"
        "      checkState(!buildCalled);\n"
        "      this.fontFamily = fontFamily;\n"
        "      return this;\n"
        "    }\n"
        "\n"
        "    /** Sets the directory that subtitle fonts are loaded from. */\n"
        "    @CanIgnoreReturnValue\n"
        "    public Builder setFontsDirectory(String fontsDirectory) {\n"
        "      checkState(!buildCalled);\n"
        "      this.fontsDirectory = fontsDirectory;\n"
        "      return this;\n"
        "    }\n"
        "\n"
        "    /**\n"
        "     * Sets the vertical position of the secondary subtitle, as a percentage of the screen\n"
        "     * height.\n"
        "     *\n"
        "     * <p>Configuring the secondary subtitle without selecting a track for it leaves it off,\n"
        "     * which is the same state as not calling this at all.\n"
        "     */\n"
        "    @CanIgnoreReturnValue\n"
        "    public Builder setSecondarySubtitlePosition(float position) {\n"
        "      checkState(!buildCalled);\n"
        "      secondarySubtitleConfigured = true;\n"
        "      secondaryPosition = position;\n"
        "      return this;\n"
        "    }\n"
        "\n"
        "    /** Sets whether the secondary subtitle ignores the ASS styles carried by the file. */\n"
        "    @CanIgnoreReturnValue\n"
        "    public Builder setSecondaryAssStyleOverride(boolean overrideAssStyles) {\n"
        "      checkState(!buildCalled);\n"
        "      secondarySubtitleConfigured = true;\n"
        "      secondaryOverrideAssStyles = overrideAssStyles;\n"
        "      return this;\n"
        "    }\n"
        "\n"
        "    public MpvSubtitleOptions build() {\n",
    ),
)

patch(
    "options/MpvSubtitleOptionDefaults.java",
    (
        '  private static final String OPT_SUBTITLE_COLOR = "sub-color";\n',
        '  private static final String OPT_SUBTITLE_COLOR = "sub-color";\n'
        '  private static final String OPT_SUBTITLE_FONT = "sub-font";\n'
        '  private static final String OPT_SUBTITLE_FONTS_DIR = "sub-fonts-dir";\n',
    ),
    (
        "    if (options.isSecondarySubtitleConfigured()) {\n"
        "      addSecondarySubtitleOptions(builder, options);\n"
        "    }\n"
        "    return builder;\n",
        "    @Nullable String fontFamily = options.getFontFamily();\n"
        "    if (fontFamily != null) {\n"
        "      addSubtitleString(builder, OPT_SUBTITLE_FONT, fontFamily);\n"
        "    }\n"
        "    @Nullable String fontsDirectory = options.getFontsDirectory();\n"
        "    if (fontsDirectory != null) {\n"
        "      addSubtitleString(builder, OPT_SUBTITLE_FONTS_DIR, fontsDirectory);\n"
        "    }\n"
        "    if (options.isSecondarySubtitleConfigured()) {\n"
        "      addSecondarySubtitleOptions(builder, options);\n"
        "    }\n"
        "    return builder;\n",
    ),
)

patch(
    "MpvPlayer.java",
    (
        "import androidx.media3.common.TrackSelectionParameters;\n",
        "import androidx.media3.common.TrackGroup;\n"
        "import androidx.media3.common.TrackSelectionOverride;\n"
        "import androidx.media3.common.TrackSelectionParameters;\n"
        "import androidx.media3.common.Tracks;\n",
    ),
    (
        "    runOnPlayerLooper(() -> subtitleController.setOptions(config));\n"
        "  }\n",
        "    runOnPlayerLooper(() -> subtitleController.setOptions(config));\n"
        "  }\n"
        "\n"
        "  /**\n"
        "   * Returns the override that selects the primary text track, or {@code null} if the primary\n"
        "   * text track is chosen automatically.\n"
        "   */\n"
        "  public @Nullable TrackSelectionOverride getPrimaryTextTrackSelectionOverride() {\n"
        "    TrackSelectionParameters parameters = trackController.getParameters();\n"
        "    Tracks tracks = trackController.getTracks();\n"
        "    TrackSelectionOverride selected = null;\n"
        "    for (TrackSelectionOverride override : parameters.overrides.values()) {\n"
        "      if (override.getType() == C.TRACK_TYPE_TEXT\n"
        "          && hasTrackGroup(tracks, override.mediaTrackGroup)) {\n"
        "        selected = override;\n"
        "      }\n"
        "    }\n"
        "    return selected;\n"
        "  }\n"
        "\n"
        "  /**\n"
        "   * Returns the override that selects the secondary text track, or {@code null} if none is\n"
        "   * selected.\n"
        "   *\n"
        "   * <p>Always {@code null} in this build. This module is built from the public fork, which\n"
        "   * has no secondary text track support: the app that consumes it was written against a\n"
        "   * private branch, and nothing published reaches mpv's secondary-sid. Reporting no\n"
        "   * secondary text track keeps this class consistent with its own candidate list, which is\n"
        "   * empty for the same reason.\n"
        "   */\n"
        "  public @Nullable TrackSelectionOverride getSecondaryTextTrackSelectionOverride() {\n"
        "    return null;\n"
        "  }\n"
        "\n"
        "  /**\n"
        "   * Returns the overrides that could be selected as the secondary text track.\n"
        "   *\n"
        "   * <p>Always empty in this build; see {@link #getSecondaryTextTrackSelectionOverride}.\n"
        "   */\n"
        "  public List<TrackSelectionOverride> getSecondaryTextTrackSelectionOverrides() {\n"
        "    return List.of();\n"
        "  }\n"
        "\n"
        "  /**\n"
        "   * Returns whether the secondary text track has been promoted to the primary one.\n"
        "   *\n"
        "   * <p>Always {@code false} in this build; see\n"
        "   * {@link #getSecondaryTextTrackSelectionOverride}.\n"
        "   */\n"
        "  public boolean isSecondaryTextTrackSuppressed() {\n"
        "    return false;\n"
        "  }\n"
        "\n"
        "  /**\n"
        "   * Sets the override that selects the secondary text track.\n"
        "   *\n"
        "   * <p>Does nothing in this build. No caller can reach it either: selections are picked from\n"
        "   * {@link #getSecondaryTextTrackSelectionOverrides}, which is empty.\n"
        "   */\n"
        "  public void setSecondaryTextTrackSelectionOverride(\n"
        "      @Nullable TrackSelectionOverride selection) {\n"
        "    // Unsupported: see getSecondaryTextTrackSelectionOverride.\n"
        "  }\n"
        "\n"
        "  /** Clears the secondary text track selection. Does nothing in this build. */\n"
        "  public void resetSecondaryTextTrackSelection() {\n"
        "    // Unsupported: see getSecondaryTextTrackSelectionOverride.\n"
        "  }\n"
        "\n"
        "  /**\n"
        "   * Enables or disables automatic selection of the secondary text track.\n"
        "   *\n"
        "   * <p>Does nothing in this build; see {@link #getSecondaryTextTrackSelectionOverride}.\n"
        "   */\n"
        "  public void setSecondaryTextTrackAutoSelectionEnabled(boolean enabled) {\n"
        "    // Unsupported: see getSecondaryTextTrackSelectionOverride.\n"
        "  }\n"
        "\n"
        "  private static boolean hasTrackGroup(Tracks tracks, TrackGroup group) {\n"
        "    for (Tracks.Group candidate : tracks.getGroups()) {\n"
        "      if (candidate.getMediaTrackGroup().equals(group)) {\n"
        "        return true;\n"
        "      }\n"
        "    }\n"
        "    return false;\n"
        "  }\n",
    ),
)

# The patch is text, so prove the result rather than trusting it: every
# member the app calls has to be there, or the failure is a runner and
# a gradle stack trace away instead of three lines above it.
EXPECTED = {
    "MpvPlayer.java": (
        "getPrimaryTextTrackSelectionOverride",
        "getSecondaryTextTrackSelectionOverride",
        "getSecondaryTextTrackSelectionOverrides",
        "isSecondaryTextTrackSuppressed",
        "setSecondaryTextTrackSelectionOverride",
        "resetSecondaryTextTrackSelection",
        "setSecondaryTextTrackAutoSelectionEnabled",
    ),
    "MpvSubtitleOptions.java": (
        "setFontFamily",
        "setFontsDirectory",
        "setSecondarySubtitlePosition",
        "setSecondaryAssStyleOverride",
    ),
    "options/MpvSubtitleOptionDefaults.java": (
        "OPT_SUBTITLE_FONT",
        "OPT_SUBTITLE_FONTS_DIR",
    ),
}
missing = []
added = 0
for name, members in EXPECTED.items():
    text = (ROOT / name).read_text(encoding="utf-8")
    for member in members:
        if member + "(" not in text and member + " " not in text:
            missing.append(name + " -> " + member)
        else:
            added += 1
if missing:
    print("::error::the patch left members missing: " + ", ".join(missing))
    sys.exit(1)
print("mpvplayer patch verified: " + str(added) + " members present")
