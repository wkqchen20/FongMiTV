# Adapted from the "ci/build-android" branch of https://github.com/qfeng3168/TV
# (.github/workflows/android-build.yml, commits 26d33af, 97ca285 and 87ba974).
# FongMi/TV and derivatives are licensed under the GNU GPL v3; see LICENSE.md.

# Run from the root of a FongMi/TV checkout at 4afc447 (5.6.3).
import os
import sys

FILES = {
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassConfiguration.java": r'''
package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;

/**
 * Stand-in for the libass configuration holder that FongMi/media does not publish.
 *
 * <p>Values are accepted and dropped. Nothing reaches libass, because
 * {@link LibassPlaybackSession#isAvailable()} is false and every call site checks it
 * first.
 */
@SuppressWarnings("unused")
public final class LibassConfiguration {

    private LibassConfiguration() {
    }

    /** Mirrors the fluent API used by ExoPlayerSession. */
    public static final class Builder {

        private String fontConfig;
        private String fontsDirectory;
        private String defaultFontFamily;
        private int maximumRenderPixels;
        private int maximumGlyphCount;
        private int maximumBitmapCacheSizeMb;

        public Builder setFontConfig(@Nullable String fontConfig) {
            this.fontConfig = fontConfig;
            return this;
        }

        public Builder setFontsDirectory(@Nullable String fontsDirectory) {
            this.fontsDirectory = fontsDirectory;
            return this;
        }

        public Builder setDefaultFontFamily(@Nullable String defaultFontFamily) {
            this.defaultFontFamily = defaultFontFamily;
            return this;
        }

        public Builder setMaximumRenderPixels(int maximumRenderPixels) {
            this.maximumRenderPixels = maximumRenderPixels;
            return this;
        }

        public Builder setMaximumGlyphCount(int maximumGlyphCount) {
            this.maximumGlyphCount = maximumGlyphCount;
            return this;
        }

        public Builder setMaximumBitmapCacheSizeMb(int maximumBitmapCacheSizeMb) {
            this.maximumBitmapCacheSizeMb = maximumBitmapCacheSizeMb;
            return this;
        }

        public LibassConfiguration build() {
            return new LibassConfiguration();
        }
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassPlaybackSession.java": r'''
package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;
import androidx.media3.common.MediaItem;
import androidx.media3.exoplayer.Renderer;
import androidx.media3.extractor.ExtractorsFactory;
import androidx.media3.extractor.text.SubtitleParser;

/**
 * Stand-in for the libass playback session that FongMi/media does not publish.
 *
 * <p>This class is where the substitution is anchored: {@link #isAvailable()} answers
 * false unconditionally, so the app never asks the missing renderer to do anything and
 * settles back onto the stock media3 subtitle path.
 */
@SuppressWarnings("unused")
public final class LibassPlaybackSession {

    /**
     * The pieces an libass-aware media source factory would need. Only the two public
     * fields read by ExoMediaSourceFactory are modelled.
     */
    public static final class MediaComponents {

        public final ExtractorsFactory extractorsFactory;
        public final SubtitleParser.Factory subtitleParserFactory;

        public MediaComponents(ExtractorsFactory extractorsFactory, SubtitleParser.Factory subtitleParserFactory) {
            this.extractorsFactory = extractorsFactory;
            this.subtitleParserFactory = subtitleParserFactory;
        }
    }

    private final LibassConfiguration configuration;
    private final boolean enabled;

    public LibassPlaybackSession(LibassConfiguration configuration, boolean enabled) {
        this.configuration = configuration;
        this.enabled = enabled;
    }

    /**
     * Always false. ExoMediaSourceFactory skips its libass media source and ExoUtil skips
     * its clock renderer on this answer alone.
     */
    public boolean isAvailable() {
        return false;
    }

    /** Unreachable while {@link #isAvailable()} is false. */
    public MediaComponents createMediaComponents(MediaItem mediaItem, ExtractorsFactory extractorsFactory) {
        throw new UnsupportedOperationException("libass is unavailable in this build");
    }

    /** Unreachable while {@link #isAvailable()} is false. */
    public Renderer createClockRenderer() {
        throw new UnsupportedOperationException("libass is unavailable in this build");
    }

    public void setPreloadMediaItem(@Nullable MediaItem mediaItem) {
    }

    public void setBottomPositionFraction(float fraction) {
    }

    public void setSecondaryBottomPositionFraction(float fraction) {
    }

    public void setFontScale(float scale, boolean apply) {
    }

    public void close() {
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassSubtitleController.java": r'''
package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;
import androidx.media3.common.TrackSelectionOverride;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.text.SecondaryTextOutput;
import androidx.media3.exoplayer.trackselection.SecondaryTextTrackSelector;

import java.util.Collections;
import java.util.List;

/**
 * Stand-in for the libass subtitle controller that FongMi/media does not publish.
 *
 * <p>Reports an empty selection so the UI shows no second subtitle track. The boolean is
 * false rather than true to match SecondarySubtitleState.EMPTY: SubtitleSettingPanel
 * reads it as secondaryPromotedToPrimary and would otherwise force the mode label to
 * "off".
 */
@SuppressWarnings("unused")
public final class LibassSubtitleController {

    public LibassSubtitleController(ExoPlayer player, LibassPlaybackSession session, SecondaryTextTrackSelector.Factory trackSelectorFactory, SecondaryTextOutput secondaryTextOutput) {
    }

    @Nullable
    public TrackSelectionOverride getPrimaryTextTrackSelectionOverride() {
        return null;
    }

    @Nullable
    public TrackSelectionOverride getSecondaryTextTrackSelectionOverride() {
        return null;
    }

    public List<TrackSelectionOverride> getSecondaryTextTrackSelectionOverrides() {
        return Collections.emptyList();
    }

    public boolean isSecondaryTextTrackSuppressed() {
        return false;
    }

    public void setSecondaryTextTrackSelectionOverride(@Nullable TrackSelectionOverride selection) {
    }

    public void setSecondaryTextTrackAutoSelectionEnabled(boolean enabled) {
    }

    public void close() {
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassFontFile.java": r'''
package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;

import java.io.File;
import java.io.IOException;

/**
 * Stand-in for the font metadata reader that FongMi/media does not publish.
 *
 * <p>Returns null, which makes ExternalFont.requireFamilyName raise "Font family name is
 * missing" and fails an external font import. Reading the font name table is a real
 * option (android.graphics.fonts.Font on API 29+) but is deliberately left out for now:
 * it would be new behaviour rather than a stub, and it would obscure whether the rest of
 * this substitution holds.
 *
 * <p>{@code throws IOException} is not decorative. ExternalFont.readFamilyName catches
 * IOException around this call, and in Java a catch block for a checked exception that
 * cannot be thrown is a compile error, so the declaration has to stay.
 */
@SuppressWarnings("unused")
public final class LibassFontFile {

    private LibassFontFile() {
    }

    @Nullable
    public static String getFamilyName(File file) throws IOException {
        return null;
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassNative.java": r'''
package androidx.media3.exoplayer.libass;

/**
 * Stand-in for the JNI entry point that libmedia3ass.so resolves by binary name.
 *
 * <p>Only referenced by proguard-rules-media.pro, to keep the name intact for the native
 * library. With libass unavailable that library is never loaded, so an empty class is
 * enough to satisfy the keep rule and R8.
 */
public final class LibassNative {

    private LibassNative() {
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassFrame.java": r'''
package androidx.media3.exoplayer.libass;

/**
 * Stand-in for a JNI value holder that libmedia3ass.so resolves by binary name. See
 * {@link LibassNative}.
 */
public final class LibassFrame {

    private LibassFrame() {
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/libass/LibassImage.java": r'''
package androidx.media3.exoplayer.libass;

/**
 * Stand-in for a JNI value holder that libmedia3ass.so resolves by binary name. See
 * {@link LibassNative}.
 */
public final class LibassImage {

    private LibassImage() {
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/trackselection/SecondaryTextTrackSelector.java": r'''
package androidx.media3.exoplayer.trackselection;

import android.content.Context;

import androidx.annotation.NonNull;

/**
 * Stand-in for the dual subtitle track selector that FongMi/media does not publish.
 *
 * <p>The real one selects tracks for a second, libass-rendered subtitle view. This one
 * selects nothing extra and delegates every call to the factory it wraps, which keeps
 * video, audio and primary subtitle selection behaving exactly as before.
 */
@SuppressWarnings("unused")
public final class SecondaryTextTrackSelector {

    private SecondaryTextTrackSelector() {
    }

    /** Delegates to the wrapped factory; the second subtitle track is simply not offered. */
    public static final class Factory implements TrackSelector.Factory {

        private final TrackSelector.Factory delegate;

        public Factory(TrackSelector.Factory delegate) {
            if (delegate == null) throw new NullPointerException("delegate");
            this.delegate = delegate;
        }

        @NonNull
        @Override
        public TrackSelector createTrackSelector(@NonNull Context context) {
            return delegate.createTrackSelector(context);
        }
    }
}
''',
    "app/src/main/java/androidx/media3/exoplayer/text/SecondaryTextOutput.java": r'''
package androidx.media3.exoplayer.text;

import androidx.media3.common.text.CueGroup;

/**
 * Stand-in for the second subtitle output that FongMi/media does not publish.
 *
 * <p>ExoRenderersFactory adds a TextRenderer over this unconditionally, so cues really do
 * arrive here. They are discarded on purpose: with libass unavailable there is no second
 * subtitle view to draw into, and discarding cannot affect the primary renderer, which
 * still receives its own separate output.
 */
public final class SecondaryTextOutput implements TextOutput {

    @Override
    public void onCues(CueGroup cueGroup) {
    }
}
''',
    "app/src/main/java/androidx/media3/ui/libass/LibassPlayerViewController.java": r'''
package androidx.media3.ui.libass;

import androidx.annotation.Nullable;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.libass.LibassPlaybackSession;
import androidx.media3.exoplayer.libass.LibassSubtitleController;
import androidx.media3.ui.CaptionStyleCompat;
import androidx.media3.ui.PlayerView;
import androidx.media3.ui.SubtitleView;

/**
 * Stand-in for the libass view controller that FongMi/media does not publish.
 *
 * <p>Drops the style override and never binds a second view. Subtitle styling is
 * unaffected: PlaybackActivity and SubtitleSettingPanel apply it through
 * SubtitleSetting.applyStyle on the stock SubtitleView, independently of this class.
 */
@SuppressWarnings("unused")
public final class LibassPlayerViewController {

    /** Mirrors the callback shape the caller passes as a method reference. */
    public interface SecondarySubtitleViewConfigurator {

        void configure(SubtitleView subtitleView);
    }

    public LibassPlayerViewController(ExoPlayer player, LibassPlaybackSession session, LibassSubtitleController controller) {
    }

    public void bind(PlayerView playerView) {
    }

    public void setStyleOverride(@Nullable CaptionStyleCompat style, @Nullable String fontFamily) {
    }

    public void setSecondarySubtitleViewConfigurator(@Nullable SecondarySubtitleViewConfigurator configurator) {
    }

    public void close() {
    }
}
''',
    "app/src/main/java/androidx/media3/ui/danmaku/DanmakuPlayerViewController.java": r'''
package androidx.media3.ui.danmaku;

import android.net.Uri;

import androidx.annotation.Nullable;
import androidx.media3.ui.PlayerView;

import okhttp3.OkHttpClient;

/**
 * Binds the danmaku controller of a {@link PlayerView} and forwards the controls that
 * PlaybackActivity drives it with.
 *
 * <p>This one is a real implementation, not a stand-in. FongMi/media publishes the whole
 * danmaku subsystem in its ui_danmaku module, and lib-ui-release.aar therefore ships a
 * PlayerView that already owns a DanmakuController, already wired to the DanmakuView in
 * exo_player_view.xml (id exo_danmaku) and already following the player through
 * setPlayer(). Only this facade was left unpublished, and every call it receives has a
 * public equivalent on PlayerView.
 *
 * <p>The setters are buffered because they arrive before the view does: PlaybackActivity
 * .configurePlayerView() runs from initView, while bind() is called later, from
 * syncPlayerView(), once the playback service has connected. Replaying them on bind is
 * what keeps the HTTP client, the configuration and the enabled flag from being lost.
 */
public final class DanmakuPlayerViewController {

    @Nullable private PlayerView playerView;
    @Nullable private OkHttpClient okHttpClient;
    @Nullable private DanmakuConfig config;
    @Nullable private Uri dataSource;
    private boolean enabled;
    private boolean enabledSet;

    /**
     * Points subsequent calls at {@code newPlayerView}'s danmaku controller.
     *
     * <p>Re-binding the same view is a no-op: syncPlayerView() runs again on every player
     * rebuild, and replaying the source each time would restart the danmaku fetch for no
     * reason. A null view only clears the reference; the controller itself belongs to the
     * PlayerView.
     */
    public void bind(@Nullable PlayerView newPlayerView) {
        if (playerView == newPlayerView) return;
        playerView = newPlayerView;
        if (newPlayerView == null) return;
        if (okHttpClient != null) newPlayerView.setDanmakuOkHttpClient(okHttpClient);
        if (enabledSet) newPlayerView.setDanmakuEnabled(enabled);
        if (config != null) newPlayerView.setDanmakuConfig(config);
        if (dataSource != null) newPlayerView.setDanmakuSource(dataSource);
    }

    public void setOkHttpClient(@Nullable OkHttpClient client) {
        okHttpClient = client;
        if (playerView != null) playerView.setDanmakuOkHttpClient(client);
    }

    public void setDataSource(@Nullable Uri uri) {
        dataSource = uri;
        if (playerView != null) playerView.setDanmakuSource(uri);
    }

    public void setConfig(DanmakuConfig config) {
        this.config = config;
        if (playerView != null) playerView.setDanmakuConfig(config);
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
        this.enabledSet = true;
        if (playerView != null) playerView.setDanmakuEnabled(enabled);
    }

    public void sendNow(String text) {
        if (playerView != null) playerView.sendDanmaku(text);
    }

    /**
     * Drops the reference without touching the controller. The PlayerView owns it and
     * tears it down on its own in setPlayer(null), which PlaybackActivity reaches through
     * detachPlayerView() one line earlier.
     */
    public void close() {
        playerView = null;
    }
}
''',
}

# Self-checks. A stub that lands in the wrong package, or that fails to
# declare the class its file name promises, would otherwise surface as a
# wall of javac errors pointing at the app sources instead of at this
# step.
normalized = {}
problems = []
for path, body in FILES.items():
    body = body.lstrip("\n")
    if not body.endswith("\n"):
        body += "\n"
    normalized[path] = body
    expected = "package " + os.path.dirname(path).replace("app/src/main/java/", "").replace("/", ".") + ";"
    actual = body.split("\n", 1)[0]
    if actual != expected:
        problems.append("%s: package line is %r, expected %r" % (path, actual, expected))
    name = os.path.basename(path)[: -len(".java")]
    if ("class " + name) not in body:
        problems.append("%s: does not declare class %s" % (path, name))
    if body.count("{") != body.count("}"):
        problems.append("%s: unbalanced braces, %d open vs %d close" % (path, body.count("{"), body.count("}")))

if problems:
    for problem in problems:
        print("::error::" + problem)
    sys.exit(1)

for path, body in normalized.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(body)
    print("wrote %s (%d lines)" % (path, len(body.splitlines())))

print("injected %d classes" % len(normalized))
